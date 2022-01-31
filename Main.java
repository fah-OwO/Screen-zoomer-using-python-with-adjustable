import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;

public class Main {
    public static final long serialVersionUID = 1L;
    public static final int fps=30;
    public static final int zoomLevel=4;
    public static final int width=100; //width & height before zoom (in pixels)
    public static final int height=100;
    public static void main(String[] args)
    {
        try {
            Thread.sleep(120);
            Robot r = new Robot();
            Dimension a= Toolkit.getDefaultToolkit().getScreenSize();
            int x =(int)(a.getWidth()/2);
            int y =(int)(a.getHeight()/2);
            x-=width/2;
            y-=height/2;
            Rectangle capture =new Rectangle(x, y, width, height);
            int newImageWidth = width * zoomLevel;
            int newImageHeight = height * zoomLevel;
            JFrame frame = new JFrame();
            frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            frame.setSize(newImageWidth, newImageHeight);
            frame.setAlwaysOnTop( true );
            frame.setLocationByPlatform( true );
            while (true)
            {
                long timeMillis=System.currentTimeMillis();
                BufferedImage Image = r.createScreenCapture(capture);
                BufferedImage resizedImage = new BufferedImage(newImageWidth, newImageHeight, BufferedImage.TYPE_INT_RGB);
                Graphics2D g = resizedImage.createGraphics();
                JPanel pane = new JPanel() {
                    @Override
                    protected void paintComponent(Graphics g) {
                        super.paintComponent(g);
                        g.drawImage(Image, 0, 0, newImageWidth, newImageHeight, null);
                    }
                };
                frame.getContentPane().removeAll();
                frame.repaint();
                frame.add(pane);
                frame.setVisible(true);
                timeMillis=System.currentTimeMillis()-timeMillis;
                Thread.sleep((timeMillis>1000/fps)?7:1000/fps-timeMillis);
            }

        }
        catch (AWTException  | InterruptedException ex) {
            System.out.println(ex);
        }

    }
}
