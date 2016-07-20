package com.example.billsu.gh;

/**
 * Created by billsu on 4/17/15.
 */
import android.app.Activity;


/**
 * Created by billsu on 4/17/15.
 */
import android.app.Activity;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class StoreActivity extends Activity {

    MediaPlayer storeSong;

    TextView scoreBoard;
    double battery;
    double fear;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.store_activity);
        scoreBoard = (TextView) findViewById(R.id.storemoney);
        scoreBoard.setText( MainActivity.money+"" );
        scoreBoard.setTextColor(-65536);

       


        storeSong = MediaPlayer.create(StoreActivity.this, R.raw.store_sound);
        storeSong.start();

    }


    public void fearUpgrade(View v) {
        if (MainActivity.money>= 10 && MainActivity.fearLevel>0){
            MainActivity.fearLevel-=300;
            MainActivity.money-=10;
            scoreBoard.setText( MainActivity.money+"" );
            scoreBoard.setTextColor(-65536);
        }



    }

    public void batteryUpgrade(View v) {
        if (MainActivity.money>= 2 && MainActivity.battery<1200){
            MainActivity.battery+=600;
            MainActivity.money-=2;
            scoreBoard.setText( MainActivity.money+"" );
            scoreBoard.setTextColor(-65536);
        }

    }

    public void startGame(View V) {
        storeSong.stop();


        this.finish(); //closes store, starts up game again
    }

}

