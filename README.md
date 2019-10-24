# played-to-death
A simple counter to put radio play numbers to song names throughout the day. Primarily for use in ranting about pop stations overplaying music

Right now it strictly listens to Energy 106 and the program must remain running to add to its count of songs and plays. Energy's api lists the last 100 songs played, about 7 hours worth. Add the command line argument '--daily' to start the count at 6am, as long as that time is within the last 100 songs. If not, it just goes as far back as it can, adding any new songs every fifteen minutes. 

To view the top twenty played songs, kill the program with control-c. 

Run with Python 2.7

## To-do
- [ ] Add more stations. This will require a look at whatever api they use to update their website 'recently played' widgets. A quick look reveals a variety of json forms. 
- [ ] Add persistence so day-by-day plays can be compared. 
- [ ] Add a way to view top plays without killing the program. 
