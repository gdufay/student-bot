# student-bot

A telegram bot to help students share informations.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
 	<li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## Getting Started

### Prerequisites

<!-- - a telegram bot token -->
<!-- - to get the next classes and events, a google account with a primary calendar should be linked -->

* pip
  ```sh
  sudo apt install python3-pip
  ```

### Installation

1. Get a telegram bot token
2. Clone the repo
   ```sh
   git clone https://github.com/gdufay/student-bot.git
   ```
3. Create a virtualenv
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```
4. Install python dependencies
  ```sh
  pip install -r requirements.txt
  ```
5. Export your telegram token
  ```sh
  export BOT_TOKEN="yourtoken"
  ```

## Usage

To launch the bot :

```sh
python3 main.py
```

### Options

- -h, --help show this help message and exit
- --credential\_file CREDENTIAL\_FILE Path to Google credentials file
- --cookie\_file COOKIE\_FILE Path to Google token storage file
- --port PORT port from where calendar is listening 

### Commands and capacity

- **/start** Display the start message
- **/help** Display the helper
- **/today** Show classes occuring today
- **/next** Show next classe
- **/events period** Show the events in the incoming period

## Roadmap

- [ ] basic commands and launch
- [ ] possibility to change language
- [ ] handle multiple calendars
- [ ] more

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the **TODO** License. See LICENSE.txt for more information.

## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
