## Project for bachelorthesis 
## DATENSCHUTZ: Anwendung von Multi-Party Computation auf Fitnesstracker mit dem MPyC -Framework

### Usage:

#### Daily steps with encrypted date (GUI implementation)
- run `python app.py`


create shares:

- go to "Administration"
- click "durchsuchen"
- choose "dailySteps_merged.csv" and upload file
- Aktion auswählen: "Create_Inputvalues"
- Aktion auswählen: "Delete_Inputvalues"

restore shares:
- go to "Sicht Versicherung"
- choose option for year and month
- click "Anzeigen"

NOTE: it takes some time bc the date is encrypted

##### change number of paties:

- go to definitions.PARTIES and change the number
- restart project and start again

#### Daily steps (only steps are encrypted)

create shares:

- store inputfile "dailySteps_merged.csv" in inputfiles_noSecDate
- run `python create_shares_without_EncDate.py -M3
- NOTE: `-M3` defines 3 parties 

restore Shares:

- run `python get_average_without_EncDate.py -M3 year month`

special options:

- definitions.YEARS_SPECIALS
- definitions.MONTHS_SPECIALS

#### Calculate GPS-distances

create shares:

- store inputfile "track_points.csv" in inputfiles_gps
- run `python create_gps_shares.py -M3`

restore shares:

- run `python get_gps_average.py -M3`


#### Benchmark files
run `cd /Benchmarks`

test the mpyc framework with variable inputs for multiplication or addition gates. 

- run `python benchmark_multiplication.py -M3` for multiplication gates with 3 nodes or
- run `python benchmark_addition.py -M5` for addition gates with 5 nodes

###### Set network latencies
- Set 3ms latency: `sudo tc qdisc add dev lo root netem delay 3ms`.
- change latency to 100ms: `sudo tc qdisc change dev lo root netem delay 100ms`
- delete latency: `sudo tc qdisc del dev lo root netem`



