//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:37:03 PM
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
fileInfo "UUID" "85017F2E-41F0-A0E1-9561-73B926A84B39";
createNode animCurveTL -n "CURVE1";
	rename -uid "FF5873C4-496C-AF95-0D0B-EB93A0F529F5";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 41 0 42 -3.4813214354995843 43 -5.9785318139667627
		 44 -17.7 45 -17.7 60 -17.7 63 0 76 0 80 0 140 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "38730A94-4B18-0DBC-3524-AA969F0A41AA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 0 16 0 21 0 26 0 46 0 64 0 141 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "78A4C77E-4793-63E4-86D1-2490362C5A7F";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 0 16 0 21 0 26 0 46 0 64 0 141 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "DDE77D83-4ACF-F215-6876-79A2279D3CF3";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 0 16 0 21 0 26 0 46 0 64 0 141 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "DF93E53D-4EB4-BF16-EBE8-309CFE7419AA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 1 16 1 21 1 26 1 46 1 64 1 141 1;
createNode animCurveTU -n "CURVE7";
	rename -uid "05164422-4781-DC81-6DE9-36AFE5B3881E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 1 16 1 21 1 26 1 46 1 64 1 141 1;
createNode animCurveTU -n "CURVE8";
	rename -uid "DBE4FEC0-497D-2309-C4EB-7FB528F06F05";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 1 16 1 21 1 26 1 46 1 64 1 141 1;
	setAttr -s 7 ".kit[0:6]"  2 9 9 9 9 9 2;
	setAttr -s 7 ".kot[0:6]"  2 5 5 5 5 5 2;
createNode animCurveTA -n "CURVE9";
	rename -uid "CD579D8B-461E-95D6-4777-4F89008E383F";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 -55 16 -55 21 -55 26 -90 29 -90 46 -90
		 64 -90 72 -90 76 -55 79 0 141 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "FAC3F1E5-4A71-6E1E-BDE5-F6944650DFF8";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 29.999999999999996 16 29.999999999999996
		 21 29.999999999999996 26 29.999999999999996 29 29.999999999999996 46 29.999999999999996
		 64 29.999999999999996 79 0 141 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "6C349FDA-4B75-70D6-8B46-71A74E445D0B";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 10 ".ktv[0:9]"  0 0 16 0 21 0 26 -59.999999999999993 29 -59.999999999999993
		 46 -59.999999999999993 64 -59.999999999999993 72 -59.999999999999993 79 0 141 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "B24185A1-462B-2E7A-1E68-7493414E4642";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  0 1 16 1 21 1 26 1 46 1 64 1 141 1;
// End