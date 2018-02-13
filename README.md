# WU_Scraper

Title: Weather Underground Grabber

Author: Lawerence Lee

## Description

This program scrapes airport weather data stored on Weather Underground's website. The data is output to a csv file and will 
be named with the aiport code and dates provided.

```
Parameters
----------
airport : str
    The code that designates a particular airport (ex. SFO is the airport
    code for San Francisco International).
start_date : str
    The date you'd like to start scraping data from.
end_date : str
    The final date you'd like to scrape data from.

Generates
---------
A csv containing the weather data you requested.
```

Copyright (c) 2018 LawerenceLee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
