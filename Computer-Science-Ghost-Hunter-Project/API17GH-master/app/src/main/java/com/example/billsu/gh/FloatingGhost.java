package com.example.billsu.gh;
/**
 * Created by AlysonI on 4/12/2015.
 * this fella floats around randomly
 */

import android.util.Log;
import android.widget.ImageView;

import java.util.Random;

public class FloatingGhost extends Ghost {


    public FloatingGhost(double startX, double startY, ImageView image, int id) {
        super(startX, startY, image, id);
        speed = 1;

    }

    public void move() {
//        Log.i("FloatingGhost", "move method says hi");
//        Log.i("FloatingGhost",this.getX()+ " " +this.getY() );

        int c = 50; //this is subject to change, just how many units the ghost will move
        Random rand = new Random();
        int n = rand.nextInt() % 4; // chooses a random direction to move in
        //  Log.i("FloatingGhost", "random = " + n);
        if (n == 0) {
            this.tX = (this.x + c);
        }
        if (n == 1) {
            this.tX = (this.x - c);
        }
        if (n == 2) {
            this.tY = (this.y + c);
        }
        if (n == 3) {
            this.tY = (this.y - c);
        }
        //this I stole from person class so if it doesn't work blame Luke
        double deltaX = this.tX - this.x;
        double deltaY = this.tY - this.y;
        double distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        double xSpeed = 0;
        double ySpeed = 0;
        if (distance > 0) {
            xSpeed = this.speed * (deltaX / distance);
            ySpeed = this.speed * (deltaY / distance);
        }
        // actually move now
        this.x = this.x + xSpeed; //* time;
        this.y = this.y + ySpeed; //* time;
        if (x < 10) {
            x = 10;
        }
        if (y < 10) {
            y = 10;
        }
        if (x > 710) {
            x = 710;
        }
        if (y > 800) {
            y = 800;
        }
        this.updateHitbox(); //so the hitBox follows the ghost
        this.updateImage();
        //Log.i("FloatingGhost", this.getX()+ " "+ this.getY());
    }
}

