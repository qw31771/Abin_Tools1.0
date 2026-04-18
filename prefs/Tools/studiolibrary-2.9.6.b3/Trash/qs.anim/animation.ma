//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Wed, May 17, 2023 05:23:47 PM
//Codeset: 936
requires maya "2022";
requires "stereoCamera" "10.0";
requires "mtoa" "4.2.1";
requires "Mayatomr" "2013.0 - 3.10.1.4 ";
requires "Riot_Li_Tool_MayaPlugin" "0.1";
currentUnit -l centimeter -a degree -t ntscf;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202102181415-29bfc1879c";
fileInfo "osv" "Windows 10 Pro v2009 (Build: 19043)";
fileInfo "UUID" "1632F32F-4B35-C5A0-8B3A-268BF3A912C0";
createNode animCurveTL -n "CURVE1";
	rename -uid "44BD19E1-4CDA-635B-C9AD-239F160AD50A";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 41 0 42 -3.4813214354995843 43 -5.9785318139667627
		 44 -17.7 45 -17.7 60 -17.7 63 0 76 0 80 0 140 0;
// End