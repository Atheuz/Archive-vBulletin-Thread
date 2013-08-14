Archive-vBulletin-Thread
========================

Create an XML file from a vBulletin thread. This XML file can then be displayed using attached xslt stylesheet.

NOTE
====
This is specifically made for SomethingAwful, and if you want to use it on a different vBulletin board,
make sure that you change the appropriate urls in

  1. main.py
  2. sheet.xsl and output/sheet.xsl
  3. Plus anywhere else you can find it.
    

To use make a config file called conf.json with the following contents:

{
    "Username":"YourUsername",
    "Password":"YourPassword"
}

with YourUsername and YourPassword replaced with appropriate login information for your SomethingAwful account.

Then you can run it using this command:

  python main.py [-h] [-tid THREAD\_ID | -t THREAD\_URL]
  
Where THREAD\_ID is the numerical ID of the thread you want to archive.
Where THREAD\_URL is the URL of the thread you want to archive.

-tid and -t are mutually exclusionary, you can only use one.


