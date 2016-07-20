package com.example.billsu.gh;

import android.graphics.Rect;
import android.widget.ImageView;

/**
 * Created by AlysonI on 4/10/2015.
 * this ghost will follow the girl where ever she goes
 */

public class StalkingGhost extends Ghost {

    private Person guy;

    public StalkingGhost(Person guy, double startX, double startY, ImageView image, int id) {
        super(startX, startY, image, id);
        this.guy = guy;
        this.speed = 0.5;
    }

    public void move() {
        this.tY = this.guy.getY(); // sets the y coordinate equal to the guy he's following
        this.tX = this.guy.getX(); // " " for the x coordinate
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
        this.updateHitbox(); //so the hitBox follows the ghost
        this.updateImage();

    }
}
