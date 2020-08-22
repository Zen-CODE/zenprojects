/**
 * This is test class to establish the mechanics behind working with zip files
 * to assist with handling them in CAMI-Apps
 * 
 * To compile this file:
 *   javac org.zencode.zip
 * 
 * This will compiled the class to a zip.class file. To run it:
 *   java -cp . org.zencode.Zip
 */
package org.zencode;


class ZipTest
{
    public static void main( String[] args ) {
        Zip myZip = new Zip("/home/fruitbat/Repos/zenprojects/java/Warrender.zip");

        // Test extractAll
        // myZip.extractAll("/home/fruitbat/Temp/");

        // Test getFileList function
        // ArrayList<String> contents = myZip.getFileList();
        // for (String fileName: contents){
        //     System.out.println(fileName);
        // }

        // Test extract_file
        myZip.extractFile("Warrender.ods", "/home/fruitbat/Temp/Warrender.ods");

    }
}
