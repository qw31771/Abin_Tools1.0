//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Thu, May 18, 2023 02:31:06 PM
//Codeset: 936
requires maya "2022";
requires "stereoCamera" "10.0";
requires "mtoa" "4.2.1";
requires "Riot_Li_Tool_MayaPlugin" "0.1";
requires "Mayatomr" "2013.0 - 3.10.1.4 ";
currentUnit -l centimeter -a degree -t ntscf;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202102181415-29bfc1879c";
fileInfo "osv" "Windows 10 Pro v2009 (Build: 19043)";
fileInfo "UUID" "F52414BF-4327-4758-E0C0-2D8E5197512F";
createNode animCurveTL -n "CURVE1";
	rename -uid "08597216-4E63-4C82-C7F1-D1925F64ECFC";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  0 0 40 0 41 -3.4813214354995843 42 -8.6586380734617894
		 43 -14.668570527991466 44 -17.7 60 -17.7 61 -11.800000000000026 62 -5.8999999999999737
		 63 0 76 0 80 0;
	setAttr -s 12 ".kit[11]"  1;
	setAttr -s 12 ".kot[0:11]"  1 2 2 2 2 2 2 2 
		2 2 2 2;
	setAttr -s 12 ".kix[11]"  1;
	setAttr -s 12 ".kiy[11]"  0;
	setAttr -s 12 ".kox[0:11]"  1 0.0047873992623483509 0.0032191541437299152 
		0.0027731763551556671 0.0054978731750959754 1 0.0028248474861875179 0.0028248474861875179 
		0.0028248474861875179 1 1 1;
	setAttr -s 12 ".koy[0:11]"  0 -0.99998854033848961 -0.99999481850987548 
		-0.99999615473905856 -0.99998488658106766 0 0.99999601011038042 0.99999601011038042 
		0.99999601011038042 0 0 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "F66A5EB3-42AF-CB86-732A-B8868BEF29E8";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 16 0 21 0 26 0 46 0 64 0 75 0 79 0 80 0;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "A67C49E4-4951-BD74-F5AC-A4850B72E8DA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 16 0 21 0 26 0 46 0 64 0 75 0 79 0 80 0;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "D4C24412-4524-BF6D-034B-F597329399C2";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 16 0 21 0 26 0 46 0 64 0 75 0 79 0 80 0;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "B54655F6-438C-7D06-1BBD-B7BD1C3CB2C7";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 16 1 21 1 26 1 46 1 64 1 75 1 79 1 80 1;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "D2264566-4E1B-FA9D-C3FA-7BA7709D061A";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 16 1 21 1 26 1 46 1 64 1 75 1 79 1 80 1;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTU -n "CURVE8";
	rename -uid "DFA827E8-4352-1AA4-6046-F282FAF1AED3";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 16 1 21 1 26 1 46 1 64 1 75 1 79 1 80 1;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[0:8]"  2 9 9 18 9 1 1 1 
		1;
	setAttr -s 9 ".kot[0:8]"  1 5 5 5 5 5 5 5 
		5;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 0 0 0 0 0 0 0 0;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "ACC43C14-4385-05BF-560C-4EBA75FA82B3";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 -9 29 -90 46 -90 64 -74.366287671684816
		 75 -74.366287671684816 79 -74.366287671684816 80 -7.4366287671684859 82 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[8:10]"  1 18 1;
	setAttr -s 11 ".kot[0:10]"  1 2 2 2 2 2 2 2 
		1 18 1;
	setAttr -s 11 ".kix[8:10]"  1 0.085294000744440809 0.038494131667402974;
	setAttr -s 11 ".kiy[8:10]"  0 0.99635582671905287 0.99925882624431828;
	setAttr -s 11 ".kox[0:10]"  1 1 0.46864979185742306 0.035345665468385593 
		1 0.73977744592445505 1 1 0.038494131667403245 0.085294000744440809 1;
	setAttr -s 11 ".koy[0:10]"  0 0 -0.88338404592339914 -0.99937514674550365 
		0 0.67285164078085602 0 0 0.99925882624431828 0.99635582671905287 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "7AF4BD8E-4BFF-48AD-959C-A789CBA64727";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 3.0000000000000004 29 29.999999999999996
		 46 29.999999999999996 64 38.740338050614774 75 38.740338050614774 79 38.740338050614774
		 80 3.8740338050614795 82 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[6:10]"  1 1 1 18 1;
	setAttr -s 11 ".kot[0:10]"  1 2 2 2 2 2 1 1 
		1 18 1;
	setAttr -s 11 ".kix[6:10]"  0.89137876316955778 1 1 0.16215508761369993 
		0.40556317877292164;
	setAttr -s 11 ".kiy[6:10]"  0.45325919799857289 0 0 -0.9867652849391253 
		-0.91406701506158894;
	setAttr -s 11 ".kox[0:10]"  1 1 0.84673301596483053 0.10551104075352301 
		1 0.89137876316955778 0.40556317877292475 0.17003386169535536 0.073747112834758002 
		0.16215508761369993 1;
	setAttr -s 11 ".koy[0:10]"  0 0 0.53201804450140799 0.99441813151164349 
		0 0.45325919799857289 -0.91406701506158761 -0.98543822022335059 -0.99727697423962292 
		-0.98676528493912541 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "9F3F8060-43B2-F97B-57A8-039EA439F8C2";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  0 0 16 0 21 0 26 -6.0000000000000009 29 -59.999999999999993
		 46 -59.999999999999993 64 -40.740155802984447 75 -40.740155802984447 79 -40.740155802984447
		 80 -4.0740155802984432 82 0;
	setAttr -s 11 ".kyts[3:10]" yes no no no no no yes no;
	setAttr -s 11 ".kit[7:10]"  1 1 18 1;
	setAttr -s 11 ".kot[0:10]"  1 2 2 2 2 2 2 1 
		1 18 1;
	setAttr -s 11 ".kix[7:10]"  1 1 0.15438986234098748 0.161911683714517;
	setAttr -s 11 ".kiy[7:10]"  0 0 0.9880100052157017 0.98680525265967756;
	setAttr -s 11 ".kox[0:10]"  1 1 0.62267699229950002 0.052977148587801462 
		1 0.6658528955186751 1 0.16191168371451989 0.07014534721003729 0.15438986234098748 
		1;
	setAttr -s 11 ".koy[0:10]"  0 0 -0.7824789858269986 -0.99859572486943193 
		0 0.7460830527021749 0 0.98680525265967722 0.99753678140947932 0.98801000521570181 
		0;
createNode animCurveTU -n "CURVE12";
	rename -uid "5C7640C8-4988-EB20-FEA7-BAB1FFBCCB18";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 16 1 21 1 26 1 46 1 64 1 75 1 79 1 80 1;
	setAttr -s 9 ".kyts[3:8]" yes no no no no yes;
	setAttr -s 9 ".kit[5:8]"  1 1 1 1;
	setAttr -s 9 ".kot[0:8]"  1 2 2 2 2 1 1 1 
		18;
	setAttr -s 9 ".kix[5:8]"  1 1 1 1;
	setAttr -s 9 ".kiy[5:8]"  0 0 0 0;
	setAttr -s 9 ".kox[0:8]"  1 1 1 1 1 1 1 1 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0 0 0 0 0 0 0;
// End