//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:38:02 PM
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
fileInfo "UUID" "9286197A-40AE-3C12-4F6B-C5A2114BB068";
createNode animCurveTL -n "CURVE1";
	rename -uid "A9CB2B1F-44F4-F49F-1F2C-4894A5983D5C";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  141 0 173 0 174 0 175 -5.9785318139667627
		 176 -9.5345231530376591 177 -13.617261576518883 178 -17.7 192 -17.7 195 0 217 0 221 0
		 281 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "7335C087-4B6E-FB4D-25F4-29939154EC8C";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 0 157 0 162 0 167 0 187 0 206 0 282 0;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "F2E18B9D-4C64-1FCB-0D13-0B8A11584E66";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 0 157 0 162 0 167 0 187 0 206 0 282 0;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "64686B6A-4607-64EC-A681-3F999871A9D0";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 0 157 0 162 0 167 0 187 0 206 0 282 0;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "C11E0BFF-4E81-6955-3C18-CCB9BEDE8CFF";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 1 157 1 162 1 167 1 187 1 206 1 282 1;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "1D1632F3-459E-763F-7416-4AB2E7C9B220";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 1 157 1 162 1 167 1 187 1 206 1 282 1;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
createNode animCurveTU -n "CURVE8";
	rename -uid "95F61560-462D-DD60-FD65-87B83CB2AF8E";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 1 157 1 162 1 167 1 187 1 206 1 282 1;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[0:6]"  2 9 9 1 1 18 2;
	setAttr -s 7 ".kot[0:6]"  2 5 5 5 5 5 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[6]"  1;
	setAttr -s 7 ".koy[6]"  0;
createNode animCurveTA -n "CURVE9";
	rename -uid "59057630-433A-1808-43BA-B69715611727";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 10 ".ktv[0:9]"  141 0 157 0 162 0 167 -90 170 -90 187 -90
		 204 -90 206 -45 210 0 282 0;
	setAttr -s 10 ".kyts[7:9]" yes no no;
	setAttr -s 10 ".kit[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kot[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kix[4:9]"  1 1 1 0.063533361910967326 0.063533361910967076 
		1;
	setAttr -s 10 ".kiy[4:9]"  0 0 0 0.99797971518678175 0.99797971518678175 
		0;
	setAttr -s 10 ".kox[4:9]"  1 1 0.06353336191096752 0.063533361910967326 
		1 1;
	setAttr -s 10 ".koy[4:9]"  0 0 0.99797971518678175 0.99797971518678175 
		0 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "2BE92C2D-434A-DDDD-8206-EDBB1E1219F8";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 10 ".ktv[0:9]"  141 0 157 0 162 0 167 29.999999999999996
		 170 29.999999999999996 187 29.999999999999996 204 42.026086217965705 206 21.013043108982853
		 210 0 282 0;
	setAttr -s 10 ".kyts[7:9]" yes no no;
	setAttr -s 10 ".kit[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kot[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kix[4:9]"  1 1 0.80353242726805751 0.13508422587249769 
		0.13508422587249674 1;
	setAttr -s 10 ".kiy[4:9]"  0 0 0.59526098337511058 -0.99083411927548604 
		-0.99083411927548615 0;
	setAttr -s 10 ".kox[4:9]"  1 0.80353242726805751 0.13508422587249763 
		0.13508422587249766 1 1;
	setAttr -s 10 ".koy[4:9]"  0 0.59526098337511058 -0.99083411927548604 
		-0.99083411927548593 0 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "2E96838C-4E3E-B30F-950F-74B9C43916A4";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 10 ".ktv[0:9]"  141 0 157 0 162 0 167 -59.999999999999993
		 170 -59.999999999999993 187 -59.999999999999993 204 -59.999999999999993 206 -29.999999999999993
		 210 0 282 0;
	setAttr -s 10 ".kyts[7:9]" yes no no;
	setAttr -s 10 ".kit[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kot[4:9]"  1 1 1 18 1 2;
	setAttr -s 10 ".kix[4:9]"  1 1 1 0.095060525440806884 0.095060525440806842 
		1;
	setAttr -s 10 ".kiy[4:9]"  0 0 0 0.99547149457074757 0.99547149457074757 
		0;
	setAttr -s 10 ".kox[4:9]"  1 1 0.095060525440807439 0.09506052544080687 
		1 1;
	setAttr -s 10 ".koy[4:9]"  0 0 0.99547149457074746 0.99547149457074735 
		0 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "EE75FED7-4212-4D73-7F22-F6BB21ADF41B";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 7 ".ktv[0:6]"  141 1 157 1 162 1 167 1 187 1 206 1 282 1;
	setAttr -s 7 ".kyts[5:6]" yes no;
	setAttr -s 7 ".kit[3:6]"  1 1 18 1;
	setAttr -s 7 ".kot[3:6]"  1 1 18 1;
	setAttr -s 7 ".kix[3:6]"  1 1 1 1;
	setAttr -s 7 ".kiy[3:6]"  0 0 0 0;
	setAttr -s 7 ".kox[3:6]"  1 1 1 0;
	setAttr -s 7 ".koy[3:6]"  0 0 0 0;
// End