//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Wed, May 24, 2023 11:15:39 AM
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
fileInfo "UUID" "48BC069B-4568-856E-5D36-12A82605EC82";
createNode animCurveTL -n "CURVE1";
	rename -uid "031CFA2A-4804-E2DB-0F67-A8968FED8A6D";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 14 ".ktv[0:13]"  0 0 141 0 173 0 174 0 175 -5.9785318139667627
		 176 -9.5345231530376591 177 -13.617261576518883 178 -17.7 192 -17.7 195 0 217 0 221 0
		 270 0 281 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "CFF99E3E-4777-3FD8-71C9-67822D6C879C";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 141 0 157 0 162 0 167 0 187 0 206 0
		 270 0 282 0;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "87BC536B-46BB-CEC7-EDD0-F6860CEEB616";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 141 0 157 0 162 0 167 0 187 0 206 0
		 270 0 282 0;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "4D5ADD8E-4CAE-A7DC-65F5-8181FF242A73";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 0 141 0 157 0 162 0 167 0 187 0 206 0
		 270 0 282 0;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "8550BD79-48D1-7924-A6B9-CBA65445FC9C";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 141 1 157 1 162 1 167 1 187 1 206 1
		 270 1 282 1;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "A46EC11B-4945-07F0-0433-43833FB80ADE";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 141 1 157 1 162 1 167 1 187 1 206 1
		 270 1 282 1;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
createNode animCurveTU -n "CURVE8";
	rename -uid "282875D9-4B76-BF3F-1D8C-FD8A1DC4D3CC";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 141 1 157 1 162 1 167 1 187 1 206 1
		 270 1 282 1;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[0:8]"  9 2 9 9 1 1 18 9 
		2;
	setAttr -s 9 ".kot[1:8]"  2 5 5 5 5 5 5 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[8]"  1;
	setAttr -s 9 ".koy[8]"  0;
createNode animCurveTA -n "CURVE9";
	rename -uid "B9A483B5-45B6-778D-A2DD-28945E0D1F4E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  0 0 141 0 157 0 162 0 167 -90 170 -90 187 -90
		 204 -90 206 -45 210 0 270 0 282 0;
	setAttr -s 12 ".kyts[8:11]" yes no no no;
	setAttr -s 12 ".kit[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kot[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kix[5:11]"  1 1 1 0.063533361910967326 0.063533361910967076 
		1 1;
	setAttr -s 12 ".kiy[5:11]"  0 0 0 0.99797971518678175 0.99797971518678175 
		0 0;
	setAttr -s 12 ".kox[5:11]"  1 1 0.06353336191096752 0.063533361910967326 
		1 1 1;
	setAttr -s 12 ".koy[5:11]"  0 0 0.99797971518678175 0.99797971518678175 
		0 0 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "940CEA65-4EE9-0E86-958A-96AA75BADEAD";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  0 0 141 0 157 0 162 0 167 29.999999999999996
		 170 29.999999999999996 187 29.999999999999996 204 42.026086217965705 206 21.013043108982853
		 210 0 270 0 282 0;
	setAttr -s 12 ".kyts[8:11]" yes no no no;
	setAttr -s 12 ".kit[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kot[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kix[5:11]"  1 1 0.80353242726805751 0.13508422587249769 
		0.13508422587249674 1 1;
	setAttr -s 12 ".kiy[5:11]"  0 0 0.59526098337511058 -0.99083411927548604 
		-0.99083411927548615 0 0;
	setAttr -s 12 ".kox[5:11]"  1 0.80353242726805751 0.13508422587249763 
		0.13508422587249766 1 1 1;
	setAttr -s 12 ".koy[5:11]"  0 0.59526098337511058 -0.99083411927548604 
		-0.99083411927548593 0 0 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "94856048-43E4-7375-6029-849775206DB1";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  0 0 141 0 157 0 162 0 167 -59.999999999999993
		 170 -59.999999999999993 187 -59.999999999999993 204 -59.999999999999993 206 -29.999999999999993
		 210 0 270 0 282 0;
	setAttr -s 12 ".kyts[8:11]" yes no no no;
	setAttr -s 12 ".kit[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kot[5:11]"  1 1 1 18 1 2 2;
	setAttr -s 12 ".kix[5:11]"  1 1 1 0.095060525440806884 0.095060525440806842 
		1 1;
	setAttr -s 12 ".kiy[5:11]"  0 0 0 0.99547149457074757 0.99547149457074757 
		0 0;
	setAttr -s 12 ".kox[5:11]"  1 1 0.095060525440807439 0.09506052544080687 
		1 1 1;
	setAttr -s 12 ".koy[5:11]"  0 0 0.99547149457074746 0.99547149457074735 
		0 0 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "AF330B37-43EA-357D-1B06-358DB734B55E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  0 1 141 1 157 1 162 1 167 1 187 1 206 1
		 270 1 282 1;
	setAttr -s 9 ".kyts[6:8]" yes no no;
	setAttr -s 9 ".kit[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kot[4:8]"  1 1 18 2 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 1 1;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0 0;
	setAttr -s 9 ".kox[4:8]"  1 1 1 1 0;
	setAttr -s 9 ".koy[4:8]"  0 0 0 0 0;
// End