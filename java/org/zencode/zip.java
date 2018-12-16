/**
 * This is test class to establish the mechanics behind working with zip files
 * to assist with handling them in CAMI-Apps
 * 
 * To compile this file:
 *   javac zip.java
 * 
 * This will compiled the class to a zip.class file. To run it:
 *   java -cp . Zip
 */
package org.zencode;
//import java.util.List;
import java.util.ArrayList;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;


class Zip
{
    /**
     * The full path to the zip file to to extracted/examined.
     */
    public String zipFile;

    /**
     * The class constructor
     * @param zipFile - The path to the zip to be opened or examined.
     */
    public Zip(String zipFile){
        this.zipFile = zipFile;

    }

    public static void main( String[] args ) {
        System.out.println("Hello World!");
        Zip myZip = new Zip("Warrender.zip");
        myZip.extractFile("/home/fruitbat/Temp/");

        ArrayList<String> contents = myZip.getFileList();
        for (String fileName: contents){
            System.out.println(fileName);
        }
    }

    /**
     * Extracts the contents of zip file given by 'zipPath' and extracts the 
     * contents to the 'destination' folder
     * 
     * @params zipPath The full path to the zip file.
     * @params destination The folder to extract the contents to.
     */
    public void extractFile(String destination) {
        try {
            FileInputStream inputStream = new FileInputStream(this.zipFile);
            ZipInputStream zipStream = new ZipInputStream(inputStream);
            ZipEntry zEntry = null;
            while ((zEntry = zipStream.getNextEntry()) != null) {

                if (zEntry.isDirectory()) {
                    handleDirectory(zEntry.getName(), destination);
                } else {
                    FileOutputStream fout = new FileOutputStream(
                            destination + "/" + zEntry.getName());
                    BufferedOutputStream bufout = new BufferedOutputStream(fout);
                    byte[] buffer = new byte[1024];
                    int read = 0;
                    while ((read = zipStream.read(buffer)) != -1) {
                        bufout.write(buffer, 0, read);
                    }

                    zipStream.closeEntry();
                    bufout.close();
                    fout.close();
                }
            }
            zipStream.close();
            System.out.println("Unzip: Unzipping complete. path :  " + destination);
        } catch (Exception e) {
            System.out.println("Unzip: Unzipping failed");
            e.printStackTrace();
        }

    }

    /**
     * Return a list of strins specifying the contents of the zip
     * 
     * @return A list of files and folders in the zip
     */
    public ArrayList<String> getFileList(){

        ArrayList<String> contents = new ArrayList<String>();
        try {
            FileInputStream inputStream = new FileInputStream(this.zipFile);
            ZipInputStream zipStream = new ZipInputStream(inputStream);
            ZipEntry zEntry = null;
            while ((zEntry = zipStream.getNextEntry()) != null) {
                contents.add(zEntry.getName());
            }
            zipStream.close();
        } catch (Exception e) {
            System.out.println("Unzip: Unzipping failed");
            e.printStackTrace();
    }
    return contents;
}

    private static void handleDirectory(String dir, String destination) {
        File f = new File(destination + dir);
        if (!f.isDirectory()) {
            f.mkdirs();
        }
    }
}
