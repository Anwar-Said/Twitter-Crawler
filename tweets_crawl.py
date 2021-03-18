import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv 
import networkx as nx


ckey = ''
csecret = ''
atoken = '-'
asecret = ''


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api =  tweepy.API(auth, wait_on_rate_limit=True)
# twitter_stream = Stream(auth, Listener())
# twitter_stream.filter(track= ["Election2018"])


edge_list = open("edge_list.csv",'a')
names = ["GayTip","manuelaforster","AgeAttraction","ihealthcoach_hh","Mehriel","m_basler","Msouveranitat","ddbnews",
"TeamKenFM","pepper46477330","querdenken2161","deutsch365","reitschuster","donjoschi","Ich2ES","manuelaforster",
"AndreaSchlegel3","ghostlion27","Sei_selbst","paul_schreyer"]
for n in names:
    first_hop_count = 0
    followers = tweepy.Cursor(api.followers, screen_name =n)
    for follower in followers.items():
        try:
            influencer_id=follower.id
            s_name = follower.screen_name
            edge_list.write(n+",")
            edge_list.write(str(s_name))
            edge_list.write('\n')
            edge_list.flush()
            first_hop_count +=1
            if first_hop_count>200:
                break
            # print(first_hop_count)
            two_hops = tweepy.Cursor(api.followers, screen_name =s_name)
            two_hop_count = 0
            try:
                for f in two_hops.items():
                    two_hop_sname = f.screen_name
                    edge_list.write(str(s_name)+",")
                    edge_list.write(str(two_hop_sname))
                    edge_list.write('\n')
                    two_hop_count +=1
                    edge_list.flush()
                    # print("two hop count:",two_hop_count)
                    if two_hop_count>50:
                        break
            except tweepy.TweepError:
                print("skipped")
                
            if first_hop_count%10 == 0:
                print("{} number of followers traversed!".format(first_hop_count))
        except tweepy.TweepError as e:
            print(e.reason)
            continue
        
edge_list.close()
