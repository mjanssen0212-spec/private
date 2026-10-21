
set CLASSPATH=.\;%JAVA_HOME%\lib;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar

javac Example.java 

java  Example blabla

java  Example 7a7a7a7a7a7a7a7a

javac MagicStringsTest.java 

java org.junit.runner.JUnitCore MagicStringsTest


@rem Alternativ Klassenpfad im Befehl angeben:

@rem javac -cp .\;%JAVA_HOME%\lib Example.java 

@rem java -cp .\;%JAVA_HOME%\lib Example blabla

@rem javac -cp .\;%JAVA_HOME%\lib;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar MagicStringsTest.java 

@rem java -cp .\;%JAVA_HOME%\lib;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar org.junit.runner.JUnitCore MagicStringsTest

