//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:52:56 PM
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
fileInfo "UUID" "EDC73BE1-415C-AAD9-00A3-ABA0586A1267";
createNode animCurveTL -n "CURVE1";
	rename -uid "41A1CD2B-426F-368F-C519-83AEA79902DA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  141 0 173 0 174 0 175 -5.9785318139667627
		 176 -9.5345231530376591 177 -13.617261576518883 178 -17.7 192 -17.7 195 0 217 0 221 0
		 281 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "A8EFD529-4EFC-85D9-7A6C-06AE413B0E29";
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
	rename -uid "9AD8D6A0-4D97-4E6C-B0EB-379A068C7E38";
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
	rename -uid "0759CB70-49B7-024E-204D-56AC741445E2";
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
	rename -uid "061C9F6B-482F-545F-7251-36A897F83867";
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
	rename -uid "94D9AE4B-4313-1C68-1A98-5690874A1078";
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
	rename -uid "48947CCB-4FDA-4430-76F0-24B308CE41D6";
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
	rename -uid "97240978-465D-C5B6-502F-32BA1C9E4E36";
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
	rename -uid "23F8E851-40AD-A699-89D8-6BA178B820A4";
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
	rename -uid "A62679A8-4269-4F77-F83D-8A80077FB34A";
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
	rename -uid "2F5B3F8A-4DE0-AFB3-E0D0-E09B9B30EFF9";
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