//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:37:27 PM
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
fileInfo "UUID" "88B3CF78-419D-9B4C-A604-D386E4A54627";
createNode animCurveTL -n "CURVE1";
	rename -uid "3D96C38B-4F8F-BA18-0E73-50A92AFC7531";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  0 0 40 0 41 -3.4813214354995843 42 -8.6586380734617894
		 43 -14.668570527991466 44 -17.7 60 -17.7 61 -11.800000000000026 62 -5.8999999999999737
		 63 0 76 0 80 0 108 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "5284F6E0-4155-093D-9D94-CC941AE4010F";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 0 46 0 60 0 64 0 75 0 79 0
		 80 0 108 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "9AD23095-4C13-1BD5-D0A7-958834A76CDB";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 0 46 0 60 0 64 0 75 0 79 0
		 80 0 108 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "F338B6D2-4FF3-DC47-3454-B5A0618DD9FF";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 0 46 0 60 0 64 0 75 0 79 0
		 80 0 108 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "DA30E0A4-4D3C-859F-138E-5B91C91624E8";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 1 16 1 21 1 26 1 46 1 60 1 64 1 75 1 79 1
		 80 1 108 1;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "FF03DEAF-4CF8-D5C8-546E-73B9E265D266";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 1 16 1 21 1 26 1 46 1 60 1 64 1 75 1 79 1
		 80 1 108 1;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE8";
	rename -uid "189A9A50-4183-8C42-758D-8B957ADA6778";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 1 16 1 21 1 26 1 46 1 60 1 64 1 75 1 79 1
		 80 1 108 1;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[0:10]"  2 9 9 18 9 9 1 1 
		1 18 9;
	setAttr -s 11 ".kot[0:10]"  2 5 5 5 5 5 5 5 
		5 5 5;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "C392C431-4CE1-0181-5A04-F7B04A0C8CDD";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  0 0 16 0 21 0 26 -9 29 -90 46 -90 60 -77.840445966865957
		 64 -74.366287671684816 75 -74.366287671684816 79 -74.366287671684816 80 -7.4366287671684859
		 82 0 108 0;
	setAttr -s 13 ".kyts[3:12]" yes no no no no no no yes no no;
	setAttr -s 13 ".kit[9:12]"  1 18 1 2;
	setAttr -s 13 ".kot[9:12]"  1 18 1 2;
	setAttr -s 13 ".kix[9:12]"  1 0.085294000744440809 0.038494131667402974 
		1;
	setAttr -s 13 ".kiy[9:12]"  0 0.99635582671905287 0.99925882624431828 
		0;
	setAttr -s 13 ".kox[9:12]"  0.038494131667403245 0.085294000744440809 
		1 1;
	setAttr -s 13 ".koy[9:12]"  0.99925882624431828 0.99635582671905287 
		0 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "B509A6CD-409B-DA6D-7AD6-E1B538E18DD1";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  0 0 16 0 21 0 26 3.0000000000000004 29 29.999999999999996
		 46 29.999999999999996 60 36.79804070603371 64 38.740338050614774 75 38.740338050614774
		 79 38.740338050614774 80 3.8740338050614795 82 0 108 0;
	setAttr -s 13 ".kyts[3:12]" yes no no no no no no yes no no;
	setAttr -s 13 ".kit[7:12]"  1 1 1 18 1 2;
	setAttr -s 13 ".kot[7:12]"  1 1 1 18 1 2;
	setAttr -s 13 ".kix[7:12]"  0.89137876316955778 1 1 0.16215508761369993 
		0.40556317877292164 1;
	setAttr -s 13 ".kiy[7:12]"  0.45325919799857289 0 0 -0.9867652849391253 
		-0.91406701506158894 0;
	setAttr -s 13 ".kox[7:12]"  0.40556317877292475 0.17003386169535536 
		0.073747112834758002 0.16215508761369993 1 1;
	setAttr -s 13 ".koy[7:12]"  -0.91406701506158761 -0.98543822022335059 
		-0.99727697423962292 -0.98676528493912541 0 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "7780B50D-48F2-E998-29F5-369CD44B527E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 13 ".ktv[0:12]"  0 0 16 0 21 0 26 -6.0000000000000009 29 -59.999999999999993
		 46 -59.999999999999993 60 -45.020121180099018 64 -40.740155802984447 75 -40.740155802984447
		 79 -40.740155802984447 80 -4.0740155802984432 82 0 108 0;
	setAttr -s 13 ".kyts[3:12]" yes no no no no no no yes no no;
	setAttr -s 13 ".kit[8:12]"  1 1 18 1 2;
	setAttr -s 13 ".kot[8:12]"  1 1 18 1 2;
	setAttr -s 13 ".kix[8:12]"  1 1 0.15438986234098748 0.161911683714517 
		1;
	setAttr -s 13 ".kiy[8:12]"  0 0 0.9880100052157017 0.98680525265967756 
		0;
	setAttr -s 13 ".kox[8:12]"  0.16191168371451989 0.07014534721003729 
		0.15438986234098748 1 1;
	setAttr -s 13 ".koy[8:12]"  0.98680525265967722 0.99753678140947932 
		0.98801000521570181 0 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "8FDE01B3-4491-459B-9436-3184D59C3B73";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 1 16 1 21 1 26 1 46 1 60 1 64 1 75 1 79 1
		 80 1 108 1;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kot[6:10]"  1 1 1 18 2;
	setAttr -s 11 ".kix[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".kiy[6:10]"  0 0 0 0 0;
	setAttr -s 11 ".kox[6:10]"  1 1 1 1 1;
	setAttr -s 11 ".koy[6:10]"  0 0 0 0 0;
// End