/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package twitterreview;

/**
 *
 * @author Srija
 */
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import twitter4j.FilterQuery;
import twitter4j.GeoLocation;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.conf.ConfigurationBuilder;
public class TwitterReview {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
         double lat= 35.7847 ;       // latitude and longotude of empire state building
        double longitude = 78.6821 ;
        //authentication
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true)
          .setOAuthConsumerKey("DGh9KwPCvFwmOGHoBajHaCEIP")
          .setOAuthConsumerSecret("h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc")
          .setOAuthAccessToken("963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP")
          .setOAuthAccessTokenSecret("lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3");
        
//        TwitterStreamFactory tf = new TwitterStreamFactory(cb.build());
//        TwitterStream twitterStream = tf.getInstance();
            TwitterFactory tf = new TwitterFactory(cb.build());
            Twitter twitter = tf.getInstance();
            int counter =0;
//                StatusListener listener = new StatusListener(){
//            public void onStatus(Status status) {
                try {
                    
                    GeoLocation location = new GeoLocation(lat, longitude);
                    
                    Query query = new Query ("appears");
                    query.setGeoCode(location, 100, Query.KILOMETERS); //setting search code within 0 miles
                    
                    do {
                    QueryResult result = twitter.search(query);
                    System.out.println("---" + result.getQuery()  );
                    
                    
                        
                        
                        //result = twitter.search(query);
                        
                        List<Status> tweets = result.getTweets();
                        
                        for (Status tweet : tweets) {
                            System.out.println(tweet.getUser().getName() + " : " + tweet.getText()+ "  Tweeted AT: " + tweet.getCreatedAt()+"Location :"+location);
                            System.out.println("-----------------------------------------------------------------------------------");
                        counter ++;
                        }
                        query = result.nextQuery();
                        
                    } while (query != null);
                    System.out.println("----number of tweets"+ counter);
                } catch (TwitterException ex) {
                    Logger.getLogger(TwitterReview.class.getName()).log(Level.SEVERE, null, ex);
                }
                
//            //public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}
//            //public void onTrackLimitationNotice(int numberOfLimitedStatuses) {}
////            public void onException(Exception ex) {
////                ex.printStackTrace();
////            }
//            @Override
//            public void onScrubGeo(long arg0, long arg1) {
//                // TODO Auto-generated method stub
//                
//            }
//            @Override
//            public void onStallWarning(StallWarning arg0) {
//                // TODO Auto-generated method stub
//
//            }
//  };



//twitterStream.addListener(listener);
        
//        FilterQuery filter = new FilterQuery();
//        String[] keywordsArray = { "New Year" }; //filter based on your choice of keywords
//        filter.track(keywordsArray);
//        twitterStream.filter(filter);  


            }
        }
      

    
    
