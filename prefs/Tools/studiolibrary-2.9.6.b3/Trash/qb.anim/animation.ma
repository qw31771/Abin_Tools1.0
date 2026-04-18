//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Wed, May 17, 2023 05:23:58 PM
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
fileInfo "UUID" "501A94B0-41D2-78E1-FB0B-C5AA39ED9EB0";
createNode animCurveTL -n "CURVE1";
	rename -uid "CE17A117-4192-D284-0E5B-09909236C8F8";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 0 15 0 20 0 25 0 45 0 63 0 140 0;
createNode animCurveTL -n "CURVE2";
	rename -uid "CFEA4174-4328-B3F7-AC43-4591CF7F805E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 0 15 0 20 0 25 0 45 0 63 0 140 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "ED37F548-4ACC-BA43-8EAA-05BA38C8D567";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 0 15 0 20 0 25 0 45 0 63 0 140 0;
createNode animCurveTU -n "CURVE4";
	rename -uid "C261D29D-42C1-18E0-53DF-1A88A13AA956";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 1 15 1 20 1 25 1 45 1 63 1 140 1;
createNode animCurveTU -n "CURVE5";
	rename -uid "A13F97DA-43C4-E39D-03A1-948AE3AE19A6";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 1 15 1 20 1 25 1 45 1 63 1 140 1;
createNode animCurveTU -n "CURVE6";
	rename -uid "BE0162D1-4C50-F981-D29B-959BAC2FA22E";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 1 15 1 20 1 25 1 45 1 63 1 140 1;
	setAttr -s 7 ".kit[0:6]"  2 9 9 9 9 9 2;
	setAttr -s 7 ".kot[0:6]"  2 5 5 5 5 5 2;
createNode animCurveTA -n "CURVE7";
	rename -uid "09491156-4716-7E45-67D9-E1B42EDB596F";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  -1 -55 15 -55 20 -55 25 -90 28 -90 45 -90
		 63 -90 71 -90 75 -55 78 0 140 0;
createNode animCurveTA -n "CURVE8";
	rename -uid "180CDF7A-4B5D-0736-8092-C0A702626D5F";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  -1 29.999999999999996 15 29.999999999999996
		 20 29.999999999999996 25 29.999999999999996 28 29.999999999999996 45 29.999999999999996
		 63 29.999999999999996 78 0 140 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "33761D23-4289-3948-D511-E2A0860049DA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 10 ".ktv[0:9]"  -1 0 15 0 20 0 25 -59.999999999999993 28 -59.999999999999993
		 45 -59.999999999999993 63 -59.999999999999993 71 -59.999999999999993 78 0 140 0;
createNode animCurveTU -n "CURVE10";
	rename -uid "0A9E93C3-4A1C-7CAA-8035-E8BBE8186C23";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  -1 1 15 1 20 1 25 1 45 1 63 1 140 1;
// End