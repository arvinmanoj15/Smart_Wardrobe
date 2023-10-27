#include <iostream>
#include <curl/curl.h>
#include "/home/arvin/Documents/json.hpp"


using json = nlohmann::json;

const std::string API_KEY = "1095b1ef7fde7db6a9704c45519fdd18";

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
        return "It's very hot! Consider wearing light and breathable clothing like cotton shirts and shorts.";
    } else if (temperature > 20.0) {
        return "It's hot. A t-shirt and shorts should be comfortable.";
    } else if (temperature > 10.0) {
        return "It's warm. You may want to wear a light jacket over a t-shirt.";
    } else if (temperature > 5.0) {
        return "It's cool. A sweater or hoodie would be nice.";
    } else {
        return "It's cold. Dress warmly with a heavy jacket and layers.";
    }
}

int main() {
    CURL* curl;
    CURLcode res;

    struct MemoryStruct chunk;
    chunk.memory = (char*)malloc(1);
    chunk.size = 0;

    std::string city_name;

    std::cout << "Enter the city name: ";
    std::cin >> city_name;

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
