import os
from datetime import date
from datetime import datetime
from datetime import timedelta
import sys
uidcounter=0
def putlineinoutput (hour,block,length,cartnr,crtname,splength):
    global uidcounter
    uidcounter+=1
    stline='{:02d}:{:02d}:{:02d}  {}         {} {:02d}:{:02d}:{:02d} {:03d} {}    1 \n'.format(hour,minutes[block]+(seconds[block]+length)//60, (length+seconds[block])%60,cartnr.partition('_')[0],crtname[:34].ljust(34),00,splength//60,splength%60,uidcounter,'Trafficplanner'.ljust(32))
    if not f.closed: f.write(stline)
    if debug==1:
        print (stline,end='')



#### INITIALIZE VARIABLES
debug=0
block=0
p=0
stline=''
minutes=[0 for i in range(12)]
seconds=[0 for i in range(12)]
maxblocklength=[0 for i in range(12)]
maxcampaigns=20
maxspotspercampaign =12
maxspots=50
maxbumpers=12
campaignname=['' for i in range(maxcampaigns)]
weekdays=['' for i in range(maxcampaigns)]
startdate=[datetime.max for i in range(maxcampaigns)]
enddate=[datetime.min for i in range(maxcampaigns)]
starthour=['' for i in range(maxcampaigns)]
endhour=['' for i in range(maxcampaigns)]
spotpercampaign = [[0]*maxspotspercampaign for i in range(maxcampaigns)]
spotname=['' for i in range(maxspots)]
spotlength=[0 for i in range(maxspots)]
dailyfreq=[0 for i in range(maxcampaigns)]
dailyshift=[0 for i in range(maxcampaigns)]
blockshift=[0 for i in range(maxcampaigns)]
cartnumber=[0 for i in range(maxspots)]
bumpercount=-1
bumpername=[0 for i in range(maxbumpers)]
bumpercart=[''for i in range(maxbumpers)]
bumperlength=[0 for i in range(maxbumpers)]
bumpers=0
##### PARSE CONFIG FILE

print ('Parsing configuration ...')

with open('/etc/trafficplan.conf','r')as f:
    #todo make /etc/trafficplan.conf
        for line in f:
            s =line.strip().partition("#")[0].partition('block')[2].partition(':')[0].strip()
            if s:
                block=int(s)
              #  print (block)

            s =line.strip().partition("#")[0].partition('time')[2].partition('=')[2].strip().partition('m')[0]
            if s:
               # print(s)
                minutes[block]=int(s)

            s =line.strip().partition("#")[0].partition('time')[2].partition('=')[2].strip().partition('m')[2].partition('s')[0]
            if s:
                #print(s)
                seconds[block]=int(s)

            s =line.strip().partition("#")[0].partition('blcksperhour=')[2].strip()
            if s:
                blocksperhour=int(s)

            s = line.strip().partition("#")[0].partition('maxlength=')[2].strip()
            if s:
                maxblocklength[block] = int(s)

            s =line.strip().partition("#")[0].partition('logoutputpath=')[2].strip()
            if s:
                logoutputpath=s


            s =line.strip().partition("#")[0].partition('logfileform=')[2].strip()
            if s:
                logfileform=s

            s =line.strip().partition("#")[0].partition('spot=')[2].strip()
            if s:
                bumpercount += 1
                bumpercart[bumpercount]=s

            s =line.strip().partition("#")[0].partition('spotlength=')[2].strip()
            if s:
                bumperlength[bumpercount]=int(s)
            s = line.strip().partition("#")[0].partition('spotname=')[2].strip()
            if s:
                bumpername[bumpercount] = s

bumpers=bumpercount
#todo get intro and outro spots


#### CHECK PLAUSIBILITY OF VARIABLES


#### PARSE CAMPAIGN DEFINITION FILE
print ('Parsing campaign definitions ...')
campaign=0
spotcounter=0
campaigncounter=0
with open('/home/rd/Nextcloud/Peter/Trafficplan/campaigns', 'r')as f:
    #todo get filename from conffile
    for line in f:
        s = line.strip().partition("#")[0].partition('campaign')[2].partition (':')[0]
        spotpercampaign[campaign][campaigncounter+1] = -1
        if s:
            campaign=int(s)
            campaigncounter=0

        s = line.strip().partition("#")[0].partition('camp_name=')[2].strip()
        if s: campaignname[campaign]=s

        s = line.strip().partition("#")[0].partition('weekdays=')[2].strip()+'A'
        if len(s)>1: weekdays[campaign]=s

        s = line.strip().partition("#")[0].partition('spot=')[2].strip()
        if s:
            campaigncounter +=1
            spotcounter +=1
            cartnumber[spotcounter]=s
            spotpercampaign[campaign][campaigncounter]=spotcounter

        s = line.strip().partition("#")[0].partition('spotname=')[2].strip()
        if s: spotname[spotcounter] = s

        s = line.strip().partition("#")[0].partition('length=')[2].strip()
        if s: spotlength[spotcounter] = int(s)

        s = line.strip().partition("#")[0].partition('dailyfreq=')[2].strip()
        if s: dailyfreq[campaign]=int(s)

        s = line.strip().partition("#")[0].partition('dailyshift=')[2].strip()
        if s: dailyshift[campaign] = int(s)

        s = line.strip().partition("#")[0].partition('blockshift=')[2].strip()
        if s: blockshift[campaign] = int(s)

        s = line.strip().partition("#")[0].partition('startdate=')[2].strip()
        if s: startdate[campaign] = datetime.strptime(s,'%m/%d/%Y')

        s = line.strip().partition("#")[0].partition('stopdate=')[2].strip()
        if s: enddate[campaign]=datetime.strptime(s,'%m/%d/%Y')

        s = line.strip().partition("#")[0].partition('starthour=')[2].strip()
        if s: starthour[campaign] = int(s.partition(':')[0])+int(s.partition(':')[2])/60

        s = line.strip().partition("#")[0].partition('stophour=')[2].strip()
        if s:
            endhour[campaign] = int(s.partition(':')[0])+int(s.partition(':')[2])/60
            #print('campaing stophour',campaign,endhour[campaign])




#### VISUALIZE CAMPAIGNS

print ('Visualize campagains ...')

delta= (max(enddate)-min(startdate))
daycount=0
spotcount=[1 for i in range(maxcampaigns)]
while daycount<delta.days:
    daycount += 1
    dat1 = min(startdate) + timedelta(days=daycount)
    j = (dat1-datetime.strptime('01012000','%d%m%Y')).days

    weekday = datetime.strftime(dat1, '%u')

    print(datetime.strftime(dat1, '%A %d_%m_%Y'))
    s = [' ' for i in range(0, 24 * blocksperhour)]

    for i in range(0, (24 )):
        s[i*blocksperhour] = (i//10).__str__()
    print(''.join(s))
    for i in range(0, (24 )):
        s[i*blocksperhour] = (i%10).__str__()
    print(''.join(s))
    blocklength =  [0 for i in range(0, 1+24 * blocksperhour)]
    for camp in range(1, campaign + 1):

        if dat1>=startdate[camp] and dat1<=enddate[camp] and weekdays[camp].find(weekday)!=-1:

            startblock = 1+round(starthour[camp] * blocksperhour)
            endblock = 1+round(endhour[camp] * blocksperhour)
            duraton = endblock - startblock
            blockinterval = round(duraton / dailyfreq[camp])
            if blockinterval==0:blockinterval = 1


            s=['-' for i in range(0,24*blocksperhour)]
            for i in range (0,(24*blocksperhour)):
                if not(i%blocksperhour):
                    s[i]='+'


            #blockinterval=round(24*blocksperhour/dailyfreq[camp])

            hourcount = 0
            while hourcount<=23:
               blockcount=0
               while blockcount<blocksperhour:
                     blockcount += 1
                     i= blockcount + hourcount * blocksperhour

                     if i>=startblock and i<=endblock:
                         if not (round((i-blockshift[camp]+dailyshift[camp]*j))%(blockinterval)):
                             s[i-1 ] = chr(64+spotcount[camp])
                             blocklength[i] += spotlength[spotpercampaign[camp][spotcount[camp]]]
                             #if blocklength[i]>maxblocklength[blockcount]:print ('MAX BLOCKLENGTH EXCEEDED !!')
                             spotcount[camp]+= 1
                             if spotpercampaign[camp][spotcount[camp]] <0: spotcount[camp] = 1



               hourcount+=1


            print(''.join(s),campaignname[camp])
    #print(blocklength)



#### WRITE CAMPAIGNS TO FILES


delta= (max(enddate)-min(startdate))
daycount=0
spotcount=[1 for i in range(maxcampaigns)]
while daycount<delta.days:
    daycount += 1
    dat1 = min(startdate) + timedelta(days=daycount)
    datetoday = datetime.today() - timedelta(days=1)
    j = (dat1-datetime.strptime('01012000','%d%m%Y')).days
    weekday = datetime.strftime(dat1, '%u')
    blocklength =  [0 for i in range(0, 1+24 * blocksperhour)]
    #print(datetime.strftime(dat1, logfileform))

    filename=logoutputpath+datetime.strftime(dat1, logfileform).__str__()
    if dat1 > datetoday:
        print('compiling:',filename)
        f=open(filename,'w')

        hourcount=0
        while hourcount<=23:
           blockcount=0
           while blockcount<blocksperhour:

                 blockcount += 1
                 i= blockcount + hourcount * blocksperhour
                 if debug==1: print('nextblock',i,hourcount,blockcount)

                 for camp in range(1, campaign + 1):

                     if dat1 >= startdate[camp] and dat1 <= enddate[camp] and weekdays[camp].find(weekday) != -1:

                         startblock = 1+round(starthour[camp] * blocksperhour)
                         endblock = 1+round(endhour[camp] * blocksperhour)
                         duraton = endblock - startblock
                         blockinterval = round(duraton / dailyfreq[camp])
                         if blockinterval==0:blockinterval=1
                         if i>=startblock and i<=endblock:
                             if debug==1: print (i,'camp',camp,round((i-blockshift[camp]+dailyshift[camp]*j))%(blockinterval),((i-blockshift[camp]+dailyshift[camp]*j))%(blockinterval))
                             if not (round((i-blockshift[camp]+dailyshift[camp]*j))%(blockinterval)):
                                 if blocklength[i]==0:
                                     #print(r,blockcount,'intro ',end='')
                                     #if not f.closed: f.write('\n')
                                     putlineinoutput(hourcount, blockcount, blocklength[i], bumpercart[0], bumpername[0],bumperlength[0])
                                     #todo put correct intro
                                     blocklength[i] += bumperlength[0]

                                 #print(blocklength[i])
                                 #s[i-1]=spotpercampaign[camp][spotcount[camp]].__str__()
                                 #s[i - 1] = chr(64+spotcount[camp])
                                 putlineinoutput(hourcount, blockcount, blocklength[i], cartnumber[spotpercampaign[camp][spotcount[camp]]],
                                 spotname[spotpercampaign[camp][spotcount[camp]]],spotlength[spotpercampaign[camp][spotcount[camp]]])

                                 #todo shorten this line
                                 #print (cartnumber[spotpercampaign[camp][spotcount[camp]]])
                                 blocklength[i] += spotlength[spotpercampaign[camp][spotcount[camp]]]
                                 spotcount[camp]+= 1
                                 if spotpercampaign[camp][spotcount[camp]] <0: spotcount[camp] = 1
                 if blocklength[i] !=0:
                     bumpercount +=1
                     if bumpercount>bumpers:bumpercount=1
                     putlineinoutput(hourcount, blockcount, blocklength[i], bumpercart[bumpercount], bumpername[bumpercount],bumperlength[bumpercount])




           hourcount+=1
        uidcounter=0
        f.close()
    else:
        if os.path.exists(filename):
            print('removing:', filename)
            os.remove(filename)
