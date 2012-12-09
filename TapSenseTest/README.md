Ghost
=====

A coding challenge I was playing around with. It's a human vs computer word game, and it's still incomplete, but playable.

----

Optimal Ghost

In the game of Ghost, two players take turns building up an English word from left to right. Each player adds one letter per turn. The goal is to not complete the spelling of a word: if you add a letter that completes a word (of 4+ letters), or if you add a letter that produces a string that cannot be extended into a word, you lose. (Bluffing plays and "challenges" may be ignored for the purpose of this puzzle.)

Write a program that allows a user to play Ghost against the computer.

The computer should play optimally given the following dictionary: WORD.LST (1.66 MB). Allow the human to play first. If the computer thinks it will win, it should play randomly among all its winning moves; if the computer thinks it will lose, it should play so as to extend the game as long as possible (choosing randomly among choices that force the maximal game length).

----

Optimal Ghost

In the game of Ghost (http://www.kith.org/logos/words/lower/g.html), two players take turns building up an English word from left to right. Each player adds one letter per turn. The goal is to not complete the spelling of a word: if you add a letter that completes a word (of 4+ letters), or if you add a letter that produces a string that cannot be extended into a word, you lose. (Bluffing plays and "challenges" may be ignored for the purpose of this puzzle.)

Write a program that allows a user to play Ghost against the computer.

The computer should play optimally given the following dictionary: WORD.LST (1.66 MB) (http://www.itasoftware.com/careers/work-at-ita/PuzzleFiles/WORD.LST). Allow the human to play first. If the computer thinks it will win, it should play randomly among all its winning moves; if the computer thinks it will lose, it should play so as to extend the game as long as possible (choosing randomly among choices that force the maximal game length).

Your program should be written as a Java web application that provides an html-based, rich GUI for a human to play against the optimal computer player from inside the Firefox browser. The web page should access a server using JavaScript's XMLHttpRequest object, and display the results using DOM manipulation. Your GUI does not have to be complicated, but should be polished and look good.

Please submit your source code, configuration instructions, and any comments on your approach. Please also include a WAR file that we can test against Tomcat 5.5.x on Sun's J2SE 6.0. Finally, in your submission email, answer this question: if the human starts the game with 'n', and the computer plays according to the strategy above, what unique word will complete the human's victory?  

