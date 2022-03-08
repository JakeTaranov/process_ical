# Process ICAL Files
Takes in paramaters start, end, and the file we want to parse, then outputs are the valid events that fall between the start and date

* Test 1
    * Input: `one.ics`
    * Expected output: `test01.txt`
    * Command: `./process_cal3 --start=2021/2/14 --end=2021/2/14 --file=one.ics`

* Test 2
    * Input: `two.ics`
    * Expected output: `test02.txt`
    * Command: `./process_cal3 --start=2021/4/18 --end=2021/4/21 --file=two.ics`

* Test 3
    * Input: `many.ics`
    * Expected output: `test03.txt`
    * Command: `./process_cal3 --start=2021/2/1 --end=2021/3/1 --file=many.ics`

* Test 4
    * Input: `two.ics`
    * Expected output: `test04.txt`
    * Command: `./process_cal3 --start=2021/4/22 --end=2021/4/23 --file=two.ics`

* Test 5
    * Input: `diana-devops.ics`
    * Expected output: `test05.txt`
    * Command: `./process_cal3 --start=2021/2/1 --end=2021/2/1 --file=diana-devops.ics`

