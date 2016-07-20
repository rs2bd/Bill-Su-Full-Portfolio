package com.example.billsu.gh;

import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Point;
import android.graphics.Rect;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;

import android.os.Handler;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.example.billsu.gh.R;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends Activity {
    FileOutputStream outputStream;
    ImageView Radial;
    ImageView Scared_Person;
    ImageView Halo;
    Person guy;
    ArrayList<Rect> obstacles;
    ArrayList<Ghost> ghosts = new ArrayList<Ghost>();
    ArrayList<ImageView> moneys = new ArrayList<ImageView>();
    RelativeLayout layout;
    private double stressLevel = 0;
    public static double battery = 1200;
    public static double money;
    private boolean timerRunning = false;
    public static double fearLevel = 0;
    public static Boolean ENABLE_RESTART = false;
    int GhostId;
    double level;
    Timer myTimer;
    Timer myTimer2;
    MediaPlayer backgroundMusic;
    ImageView Batt;
    ImageView Meter;
    private double score = 0;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final SharedPreferences sharedPref = this.getPreferences(Context.MODE_PRIVATE);
        final SharedPreferences.Editor editor = sharedPref.edit();


        setContentView(R.layout.activity_main);
        Scared_Person = (ImageView) findViewById(R.id.Scared_Person);

        level = -20623;
        final String filename = "save.txt";


        Batt = (ImageView) findViewById(R.id.Batt);
        Meter = (ImageView) findViewById(R.id.Meter);

        //   guy = new Person((double) Scared_Person.getX(), (double) Scared_Person.getY(), (double) Scared_Person.getWidth(), (double) Scared_Person.getHeight());
        guy = new Person((double) Scared_Person.getX(), (double) Scared_Person.getY(), 50, 50);
        // Log.i("image starts at", " " + Scared_Person.getX()+" "+ Scared_Person.getY());


        Radial = (ImageView) findViewById(R.id.lanternradial);
        Radial.setX(Scared_Person.getX());
        Radial.setY(Scared_Person.getY());
        layout = (RelativeLayout) findViewById(R.id.layout);

        // Log.i("image starts at", " " + Scared_Person.getX()+" "+ Scared_Person.getY());

        backgroundMusic = MediaPlayer.create(MainActivity.this, R.raw.mansion_music);
        backgroundMusic.start();

//        ImageView ghost = new ImageView(this);
//        ghost.setImageResource(R.drawable.ghost1);
//        ghost.setVisibility(View.VISIBLE);
//
//        layout.addView(ghost)
        Halo = (ImageView) findViewById(R.id.lanternkill);

        final Button save = (Button) findViewById(R.id.save);
        save.setText("Save");

        final Button load = (Button) findViewById(R.id.load);
        load.setText("Load");

        final ImageButton Lantern = (ImageButton) findViewById(R.id.Lantern);
        Lantern.setImageResource(R.drawable.lantern_off);

        Lantern.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Halo = (ImageView) findViewById(R.id.lanternkill);
                Halo.setX(Scared_Person.getX() - 100);
                Halo.setY(Scared_Person.getY() - 80);
                if (Halo.getVisibility() == View.VISIBLE) {
                    Halo.setVisibility(View.INVISIBLE);
                    Lantern.setImageResource(R.drawable.lantern_off);
                } else {
                    Halo.setVisibility(View.VISIBLE);
                    Lantern.setImageResource(R.drawable.lantern_on);
                }
            }
        });



        save.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            editor.putInt("battery", (int)battery);
            editor.putInt("level", (int)level);
            editor.putInt("fearLevel", (int)fearLevel);
            editor.putInt("money", (int)money);
            editor.putInt("score", (int)score);
            editor.commit();
                Log.i("shared preference", "hello there" + sharedPref.getAll());
            }
        });

        load.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            battery = sharedPref.getInt("battery", (int)battery);
            level = sharedPref.getInt("level", (int)level);
            fearLevel = sharedPref.getInt("fearLevel", (int)fearLevel);
            money = sharedPref.getInt("money", 0);
            score = sharedPref.getInt("score", 0);

            }
        });


        for (int i = 0; i < 2; i++) {
            ImageView ghost = new ImageView(this);
            ghost.setImageResource(R.drawable.ghost_tiny2);
            ghost.setVisibility(View.VISIBLE);

            layout.addView(ghost);


            Ghost casper = new FloatingGhost((double) 100 + (50 * i), (double) 200 + (100 * i), ghost, i);
            ghosts.add(casper);
        }

        for (int i = 2; i < 4; i++) {
            ImageView ghost = new ImageView(this);
            ghost.setImageResource(R.drawable.ghost_tiny2);
            ghost.setVisibility(View.VISIBLE);

            layout.addView(ghost);


            Ghost casper = new StalkingGhost(this.guy, (double) 210 + (50 * i), (double) 400 + (100 * i), ghost, i);
            ghosts.add(casper);
        }
        //Difficulty Timer
        myTimer = new Timer();

        myTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                TimerMethod();
            }

        }, 15000, (int) (Math.pow(1.0005, -1 * level) + 1000));

        //Movement Timer
        myTimer2 = new Timer();
        myTimer2.schedule(new TimerTask() {
            @Override
            public void run() {
                TimerMethod2();
            }

        }, 3000, 10);


    }

    private void TimerMethod() {
        this.runOnUiThread(Timer_Tick);

    }

    private Runnable Timer_Tick = new Runnable() {
        @Override
        public void run() {
            Random rand = new Random();

            for (int i = 0; i < 3; i++) {
                ImageView ghost = new ImageView(MainActivity.this);
                ghost.setImageResource(R.drawable.ghost_tiny2);
                ghost.setVisibility(View.VISIBLE);

                layout.addView(ghost);


                Ghost casper = new FloatingGhost((double) rand.nextInt(500), (double) rand.nextInt(500), ghost, GhostId);
                GhostId += 1;
                ghosts.add(casper);
            }

            for (int i = 0; i < 3; i++) {
                ImageView ghost = new ImageView(MainActivity.this);
                ghost.setImageResource(R.drawable.ghost_tiny2);
                ghost.setVisibility(View.VISIBLE);

                layout.addView(ghost);


                Ghost casper = new StalkingGhost(MainActivity.this.guy, (double) rand.nextInt(500), (double) rand.nextInt(500), ghost, GhostId);
                GhostId += 1;
                ghosts.add(casper);
            }

            //CHANGE THIS TO MODIFY SPAWN RATE, NOT OTHER STUFF
            level += 5000;

        }
    };

    private void TimerMethod2() {
        this.runOnUiThread(Timer_Tick2);

    }

    private Runnable Timer_Tick2 = new Runnable() {
        @Override
        public void run() {
            for (Ghost g : ghosts) {
                g.move();
                for (Ghost c : ghosts) {
                    if (g.getiD() != c.getiD()) {
                        g.getHitbox().intersect(c.getHitbox());
                    }

                }
            }

        }
    };






 /*   public void onStart(){
        Handler handler = new Handler();
        handler.post(new Runnable() {
            @Override
            public void run() {
                Log.d("run","yo we are in that run thing");
            }
        });
    } */


    public boolean onTouchEvent(MotionEvent event) {
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        if (fearLevel > 1000) {
            Intent myIntent = new Intent(this, EndGame.class);
            startActivity(myIntent);
            Meter.setImageResource(R.drawable.m_9_game_over);
        } else if (fearLevel > 900) {
            Meter.setImageResource(R.drawable.m_8);
        } else if (fearLevel > 800) {
            Meter.setImageResource(R.drawable.m_7);
        } else if (fearLevel > 700) {
            Meter.setImageResource(R.drawable.m_6);
        } else if (fearLevel > 600) {
            Meter.setImageResource(R.drawable.m_5);
        } else if (fearLevel > 500) {
            Meter.setImageResource(R.drawable.m_4);
        } else if (fearLevel > 400) {
            Meter.setImageResource(R.drawable.m_3);
        } else if (fearLevel > 300) {
            Meter.setImageResource(R.drawable.m_2);
        } else if (fearLevel > 200) {
            Meter.setImageResource(R.drawable.m_1);
        } else {
            Meter.setImageResource(R.drawable.m_0);
        }


        if (event.getAction() == MotionEvent.ACTION_UP == false) {
            guy.setTarget((double) event.getX(), (double) event.getY());
            guy.move();
            for (Ghost g : ghosts) {
                g.move();

            }
        }


        Scared_Person.setX((float) guy.getX());
        Scared_Person.setY((float) guy.getY() - 147);
        Radial.setX(Scared_Person.getX() - 220);
        Radial.setY(Scared_Person.getY() - 220);
        Halo.setX(Scared_Person.getX()-100);
        Halo.setY(Scared_Person.getY()-80);

        new CountDownTimer(1000, 100) {

            public void onTick(long millisUntilFinished) {

            }

            public void onFinish() {
                if (Halo.getVisibility() == View.VISIBLE){
                battery = battery - 5;}
                timerRunning = false;
                for (Iterator<Ghost> it = ghosts.iterator(); it.hasNext(); ) {
                    Ghost g = it.next();
                    double distance = Math.hypot(g.getX(), guy.getX());
                    if (distance > 500 && distance < 1000) {
                        fearLevel += 1;
                    } else if (distance > 200) {
                        fearLevel += 2;
                    } else if (distance > 100) {
                        fearLevel += 5;
                    }


                }
            }

        }.start();

            /*    long startTime = System.currentTimeMillis();
                long timeDiff = startTime;
                while(timeDiff - startTime < 1000){
                    timeDiff = System.currentTimeMillis();
                    battery = battery - 1;
                } */


        if (battery > 1000) {
            Batt.setImageResource(R.drawable.b_6);
        } else if (battery > 800) {
            Batt.setImageResource(R.drawable.b_5);
        } else if (battery > 600) {
            Batt.setImageResource(R.drawable.b_4);
        } else if (battery > 400) {
            Batt.setImageResource(R.drawable.b_3);
        } else if (battery > 200) {
            Batt.setImageResource(R.drawable.b_2);
        } else if (battery > 0) {
            Batt.setImageResource(R.drawable.b_1);
        } else {
            Halo.setVisibility(View.INVISIBLE);

            Batt.setImageResource(R.drawable.b_0_0);


        }


        Log.i("battery is", "battery: " + battery);
        Log.i("Fear level is", "fear Level: " + fearLevel);
        for (Iterator<Ghost> it = ghosts.iterator(); it.hasNext(); ) {
            Ghost g = it.next();

            if (guy.getHitbox().intersect(g.getHitbox())
                    && Halo.getVisibility() == View.VISIBLE) {
                g.die();
                score ++;

                ImageView Money = new ImageView(this);
                Money.setImageResource(R.drawable.ectoplasm_small_trans);
                Money.setX((float) g.getX());
                Money.setY((float) g.getY());
                it.remove();
                moneys.add(Money);


                layout.addView(Money);


            }

            for (int i = 0; i < moneys.size(); i++) {
                ImageView m = moneys.get(i);
                Rect getdamoney = new Rect((int)m.getX(), (int)m.getY(), (int)m.getX() + 20,
                        (int)m.getY() + 20);
                if (guy.getHitbox().intersect(getdamoney)) {
                    m.setVisibility(View.INVISIBLE);
                    money++;
                    moneys.remove(m);
                }
            }


            g.move();
        }

        TextView scoreBoard = (TextView) findViewById(R.id.textView);
        scoreBoard.setText("You Have: " + money + " Ectoplasms");
        scoreBoard.setTextColor(-65536);

        TextView scoreBoard2 = (TextView) findViewById(R.id.textView4);
        scoreBoard2.setText("You Have Killed: " + score + " Ghosts");
        scoreBoard2.setTextColor(-65536);

        return true;

    }

    public void storeButtonClicked(View v) {

        Intent intent = new Intent(this, StoreActivity.class);


        startActivity(intent);
    }

    public void onPause() {
                super.onPause();
                backgroundMusic.pause();
            }
    public void onResume() {
        super.onResume();
        backgroundMusic.start();
    }
}