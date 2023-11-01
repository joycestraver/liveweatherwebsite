# LIVE WEATHER INFORMATION WEBSITE
    #### Video Demo:  https://youtu.be/6dXn8Q54x4U
    #### Description:
    This program is designed to provide users with up-to-the-minute weather information for cities worldwide. It offers an interactive experience for the user by combining weather data with an user interface.

    When lanching the website, the user is prompted to input a city of their choice. If they choose not to specify a city, the default city displayed is Amsterdam. The chosen city is then instantly pinpointed on a map, then the live weather of the selected city is displayed in an info panel on the left side of the website.

    One of the features is its programs ability to visualize weather conditions based on the live weather descriptions. These animations adapt to the live weather descriptions of the users's chosen city.

    Besides the live weather information, the website also has a user-friendly search history. Each time the user inputs a city, it is added to the history, using a CSV file. The history also enables users to revisit their previous searches by simply clicking on the city name. The search history also has an  "clear history" button so users can clear their search history by clicking on this button, which removes all the previous entries.

    The map.HTML file contains all the necessary code for the defining the website's layout and appearance. The file contains both HTML code as CSS.

    The core function of the website is powered by the project.py file, which contains all the code responsible for retrieving the live weather data, processing user input, and generatimg the weatther animations.

    The cities.csv file stores the search history, maintaining a record of the users entries. It is important to note that this file is being reset everytime the website is stopped, using CTRL+C. or when the user clears the search history.

    The requirements.txt file contains a list of all the external libraries that wre used to create this program.

    The statioc folder contains a collection of the png images, which are used to create the live weather animations on the website.


    In short, the Live Weather Information Website is a dynamic and user-friendly platform that combines live weather data, interactive maps, animations to offer a informative weather experience. Users can explore and learn about the weather in their chosen cities.