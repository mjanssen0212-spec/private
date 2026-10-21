

set CLASSPATH=.\;%JAVA_HOME%\lib;.\jazzer_standalone.jar;.\jazzer-junit-0.22.1.jar;.\junit5-4.6.14.jar

javac Example.java
javac MagicStringsFuzzTest.java

java  com.code_intelligence.jazzer.Jazzer --target_class=MagicStringsFuzzTest 

@rem ALTERNATIV Klassenpfad im Befehl angeben:
@rem javac -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar Example.java
@rem javac -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar;.\jazzer-junit-0.22.1.jar;.\junit5-4.6.14.jar MagicStringsFuzzTest.java

@rem java -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar;.\jazzer-junit-0.22.1.jar;.\junit5-4.6.14.jar com.code_intelligence.jazzer.Jazzer --target_class=MagicStringsFuzzTest 