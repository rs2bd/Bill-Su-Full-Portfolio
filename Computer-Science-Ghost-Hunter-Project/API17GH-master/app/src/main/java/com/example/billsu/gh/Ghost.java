package com.example.billsu.gh;

import android.graphics.Rect;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;


/**
 * Created by AlysonI on 4/10/2015.
 * my shit to do:
 * Create main ghost
 * create two ghost sub classes, follow and float
 * list of all the ghosts in main
 * use andriod, and just copy what happened with the scared person.
 */
public class Ghost {

    protected double x;
    protected double y;
    protected double tY; //targetY
    protected double tX; //targetX
    protected Rect hitbox;
    protected double width; //of the image
    protected double height; //of the image
    protected double speed;
    protected ImageView Ghost_Image;
    protected int iD;

    public Ghost(double startX, double startY, ImageView image, int id) {
        this.x = startX;
        this.y = startY;
        Ghost_Image = image;
        this.updateImage();
        // this.height = Ghost_Image.getHeight();
        //  this.width = Ghost_Image.getWidth();
        this.height = 50;
        this.width = 50;

        this.hitbox = new Rect((int) this.x + 350, (int) this.y - 300, (int) (this.x + this.width),
                (int) (this.y + this.height));
        this.tX = startX;
        this.tY = startY;
        iD = id;

    }

    //basic getters & setters---------------------------------------------------
    public double getX() {
        return this.x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return this.y;
    }

    public void setTY(double target) {
        this.tY = target;
    }

    public void setTX(double target) {
        this.tX = target;
    }

    public Rect getHitbox() {
        return this.hitbox;
    }

    public int getiD() {
        return iD;
    }

    // I call this in move, just so the hitbox follows the image
    public void updateHitbox() {
        this.hitbox = new Rect((int) this.x, (int) this.y, (int) (this.x + this.width),
                (int) (this.y + this.height));
    }

    //makes sure the pictures is following our guy
    public void updateImage() {
        //Log.i("Ghost", "updateImage says hi");
        this.Ghost_Image.setX((float) this.getX());
        this.Ghost_Image.setY((float) this.getY());
        Log.i("image is at: ", "" + this.Ghost_Image.getX());

    }

    public void die() {
        this.Ghost_Image.setVisibility(View.GONE);
    }

    // skeletal move method to make java happy
    public void move() {

    }

    public void collides(Ghost ghost) {
        Rect intersection = new Rect(this.hitbox);


        if (intersection.intersect(ghost.getHitbox())) {
            Log.i("intersection", "hello from loop");
            if (intersection.width() < intersection.height()) {
                if (this.x < ghost.getX()) {
                    this.x = this.x - intersection.width();
                }
                if (this.x > ghost.getX()) {
                    this.x = this.x + intersection.width();
                }

            }
            if (intersection.height() < intersection.width()) {
                if (this.y < ghost.getY()) {
                    this.y = this.y - intersection.height();
                }
                if (this.y > ghost.getY()) {
                    this.y = this.y + intersection.height();
                }
            }

            this.updateHitbox();
            this.updateImage();

        }
        // Log.i("collides", "this hitbox = "+ hitbox + "this intersection = " +intersection);

    }
}

