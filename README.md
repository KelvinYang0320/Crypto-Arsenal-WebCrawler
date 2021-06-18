# Crypto Arsenal WebCrawler
Automated Tools for Crypto Arsenal 2021 NTU & NTHU Competition

<font color="red">We are opposed to any improper use of this program to harm Crypto Arsenal.</br> In no event shall we be liable for any special indirect or consequential damages or any damages whatsoever resulting from this program.</br>KEEP CALM AND WRITE CODE</font>

## Installation
1. Install Python language bindings for Selenium WebDriver.\
   <code>pip install selenium</code>
2. Install [Chrome driver](https://chromedriver.chromium.org/downloads) according to your Chrome version.
* Directories structure
  ```
  \Crypto-Arsenal-WebCrawler
      \chromedriver_win32
          \chromedriver.exe
      \Fintech.py
      \runner.ipynb
      \email-password.txt (optionally, you should make this txt file by youself)
      \...      
  ```
## Usage
* Import the crawler module:\
  <code>from Fintech import crypto_arsenal_crawler</code>
* Open [Crypto Arsenal](https://crypto-arsenal.io/) with your email address and your passward:\
  <code>run = crypto_arsenal_crawler(_email-address_, _passward_)</code>
* Open all of the strategies on the website and get a list of all strategies:\
  <code>run.openStrategySpace()</code>
* Run backtest on one of the strategies:\
  <code>run.backtesting(_strategies_, _start_date_, _end_date_, _exchange_, _pairs_, _amount_)</code>\
  For example, <code>run.backtesting("RSI14v2", "2021/3/30", "2021/4/30", "BINANCE", "BTC-USDT", 100000)</code>
  * Please use something like `time.sleep(1)` to slow down the process when running lots of backtest.
* Get all records of backtesting:\
  <code>run.get_backtesting_records(_strategies_)</code>
* Remove all records of backtesting:\
  <code>run.rm_backtesting_records(_strategies_)</code>
* Also, you can follow `runner.ipynb` to learn how to use the crawler.
## Demo
![](https://github.com/KelvinYang0320/Crypto-Arsenal-WebCrawler/blob/main/demo/demo.gif)