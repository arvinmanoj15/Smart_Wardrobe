#include <iostream>
#include <curl/curl.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <cstring>
#include "json.hpp"

using json = nlohmann::json;

const std::string API_KEY = "1095b1ef7fde7db6a9704c45519fdd18"; //API Key

const std::string FIFO_PATH = "/tmp/myfifo";  //Pipe name

const int32_t rfid_values[] = {
    0, // Heavy Sweater
    1, // RFID value for 0-5°C
    2, // RFID value for 5-10°C
    3, // RFID value for 10-15°C
    4, // RFID value for 15-20°C
    5, // RFID value for 20-25°C
    6, // RFID value for 25-30°C
    7  // RFID value for above 30°C
};

struct MemoryStruct {
    char* memory;
    size_t size;
};

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t real_size = size * nmemb;
    struct MemoryStruct* mem = (struct MemoryStruct*)userp;

    char* ptr = (char*)realloc(mem->memory, mem->size + real_size + 1);
    if (ptr == NULL) {
        // Out of memory
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, real_size);
    mem->size += real_size;
    mem->memory[mem->size] = 0;

    return real_size;
}

std::string getOutfitSuggestion(double temperature) {
    if (temperature > 30.0) {
        return "It's very hot! Consider wearing loose-fitting, breathable clothing like sleeveless tops, shorts, and sandals. Don't forget a wide-brimmed hat and sunglasses.";
    } else if (temperature >= 25.0) {
        return "It's hot. Wear short-sleeve shirts, lightweight shorts or skirts, and sandals or sneakers. Apply sunscreen and wear sunglasses.";
    } else if (temperature >= 20.0) {
        return "It's warm. Opt for light sweaters or cardigans, casual pants or skirts, and comfortable shoes like loafers or ballet flats.";
    } else if (temperature >= 15.0) {
        return "It's moderate. Wear a light jacket or windbreaker, t-shirts or blouses, jeans or chinos, and comfortable walking shoes.";
    } else if (temperature >= 10.0) {
        return "It's cool. Consider a light to medium-weight jacket, long-sleeve shirts or sweaters, corduroy or khaki pants, and closed-toe shoes or sneakers.";
    } else if (temperature >= 5.0) {
        return "It's cold. Bundle up with a wool or heavy knit sweater, jeans or insulated pants, warm socks, and add a scarf and a beanie.";
    } else if (temperature >= 0.0) {
        return "It's very cold. Dress warmly with an insulated parka or heavy winter coat, thermal long underwear or base layers, fleece-lined pants, winter boots, thermal gloves, and a warm hat.";
    } else {
        return "It's freezing cold. Wear an insulated parka or heavy winter coat, thermal long underwear or base layers, fleece-lined pants, winter boots, thermal gloves, and a warm hat.";
    }
}


int main() {
    CURL* curl;
    CURLcode res;

    struct MemoryStruct chunk;
    chunk.memory = (char*)malloc(1);
    chunk.size = 0;

    std::string city_name = "Cambridge,Ontario";
    
    /*
    std::cout << "Enter the city name: ";
    std::cin >> city_name;

    */
    std::string api_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=" + API_KEY;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, api_url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&chunk);

        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            try {
                json weather_data = json::parse(chunk.memory);

                if (weather_data.find("name") != weather_data.end() &&
                    weather_data.find("main") != weather_data.end() &&
                    weather_data["main"].find("temp") != weather_data["main"].end() &&
                    weather_data.find("weather") != weather_data.end()) {

                    std::string city_name = weather_data["name"];
                    double temperature = weather_data["main"]["temp"];
                    // Convert temperature from Kelvin to Celsius
                    temperature -= 273.15;

                    bool isRaining = false;
                    bool isSunny = false;
                    for (const auto& weather : weather_data["weather"]) {
                        if (weather.find("main") != weather.end()) {
                            if (weather["main"] == "Rain") {
                                isRaining = true;
                            } else if (weather["main"] == "Clear") {
                                isSunny = true;
                            }
                        }
                    }

                    std::cout << "City: " << city_name << std::endl;
                    std::cout << "Current Temperature: " << temperature << "°C" << std::endl;

                    if (isRaining) {
                        std::cout << "It's rainy. Wear a waterproof jacket and don't forget your umbrella!" << std::endl;
                    } else if (isSunny) {
                        std::cout << "It's sunny. Remember to wear sunblock to protect your skin!" << std::endl;
                    }

                    std::string outfitSuggestion = getOutfitSuggestion(temperature);
                    std::cout << "Outfit Suggestion: " << outfitSuggestion << std::endl;

                    // Determine RFID value based on temperature range
                    int32_t rfidValueToSend = 0;

                    if (temperature < 0) {
                        rfidValueToSend = rfid_values[0];
                    } else if (temperature < 5) {
                        rfidValueToSend = rfid_values[1];
                    } else if (temperature < 10) {
                        rfidValueToSend = rfid_values[2];
                    } else if (temperature < 15) {
                        rfidValueToSend = rfid_values[3];
                    } else if (temperature < 20) {
                        rfidValueToSend = rfid_values[4];
                    } else if (temperature < 25) {
                        rfidValueToSend = rfid_values[5];
                    } else if (temperature < 30) {
                        rfidValueToSend = rfid_values[6];
                    } else {
                        rfidValueToSend = rfid_values[7];
                    }

                    // Open the named pipe for writing and send the RFID value
                    int fifo_fd = open(FIFO_PATH.c_str(), O_WRONLY);

                    if (fifo_fd == -1) {
                        std::cerr << "Error opening the named pipe for writing." << std::endl;
                        return 1;
                    }

                    write(fifo_fd, &rfidValueToSend, sizeof(rfidValueToSend));
                    
                    //close(fifo_fd);

                } else {
                    std::cerr << "City name, temperature, or weather not found in JSON response." << std::endl;
                }

            } catch (const std::exception& e) {
                std::cerr << "Error parsing JSON: " << e.what() << std::endl;
            }
        }

        free(chunk.memory);
        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
    return 0;
}

