//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:53:22 PM
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
fileInfo "UUID" "504B9C2C-4A56-E74B-AFD2-CB86C97E5A95";
createNode animCurveTL -n "CURVE1";
	rename -uid "128124FD-421B-09C9-84B4-C190B7861B10";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 11 ".ktv[0:10]"  141 0 173 0 174 0 175 -5.9785318139667627
		 176 -9.5345231530376591 177 -13.617261576518883 178 -17.7 192 -17.7 195 0 217 0 221 0;
	setAttr -s 11 ".kit[10]"  1;
	setAttr -s 11 ".kot[0:10]"  1 2 2 2 2 2 2 2 
		2 2 2;
	setAttr -s 11 ".kix[10]"  1;
	setAttr -s 11 ".kiy[10]"  0;
	setAttr -s 11 ".kox[0:10]"  1 1 0.0027877416099179558 0.0046868740724898585 
		0.0040821933879092373 0.0040821933879092373 1 0.0028248474861875053 1 1 1;
	setAttr -s 11 ".koy[0:10]"  0 0 -0.9999961142408087 -0.99998901654539618 
		-0.99999166781385918 -0.99999166781385918 0 0.99999601011038042 0 0 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "1A86DB32-4452-93DE-FDB3-C795C977A3F1";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 0 157 0 162 0 167 0 187 0 206 0;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTL -n "CURVE4";
	rename -uid "E6967559-47F1-FE3B-BB4A-1BA16120202D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 0 157 0 162 0 167 0 187 0 206 0;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTL -n "CURVE5";
	rename -uid "405B05DE-4257-1348-B941-5692C0917749";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 0 157 0 162 0 167 0 187 0 206 0;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTU -n "CURVE6";
	rename -uid "50915F00-47A7-0269-1262-719F579C5F6D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 1 157 1 162 1 167 1 187 1 206 1;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTU -n "CURVE7";
	rename -uid "DD99007C-4421-AA2A-1C50-D2AAD3A31EEB";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 1 157 1 162 1 167 1 187 1 206 1;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTU -n "CURVE8";
	rename -uid "A00FEE6A-4645-B8C7-C053-F9BDFECC70C1";
	setAttr ".tan" 5;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 1 157 1 162 1 167 1 187 1 206 1;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 9 9 1 1 1;
	setAttr -s 6 ".kot[0:5]"  1 5 5 5 5 5;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 0 0 0 0 0;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
createNode animCurveTA -n "CURVE9";
	rename -uid "B352DAE1-4C92-72FC-BEA2-95BDF25C2764";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  141 0 157 0 162 0 167 -90 170 -90 187 -90
		 204 -90 206 -45 210 0;
	setAttr -s 9 ".kyts[7:8]" yes no;
	setAttr -s 9 ".kit[0:8]"  2 2 2 2 1 1 1 18 
		1;
	setAttr -s 9 ".kot[1:8]"  2 2 2 1 1 1 18 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 0.063533361910967326 0.063533361910967076;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0.99797971518678175 0.99797971518678175;
	setAttr -s 9 ".kox[0:8]"  1 1 0.052977148587801282 1 1 1 0.06353336191096752 
		0.063533361910967326 1;
	setAttr -s 9 ".koy[0:8]"  0 0 -0.99859572486943182 0 0 0 0.99797971518678175 
		0.99797971518678175 0;
createNode animCurveTA -n "CURVE10";
	rename -uid "12879F7C-4CAB-BD50-AF45-368457A1D94D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  141 0 157 0 162 0 167 29.999999999999996
		 170 29.999999999999996 187 29.999999999999996 204 42.026086217965705 206 21.013043108982853
		 210 0;
	setAttr -s 9 ".kyts[7:8]" yes no;
	setAttr -s 9 ".kit[0:8]"  2 2 2 2 1 1 1 18 
		1;
	setAttr -s 9 ".kot[1:8]"  2 2 2 1 1 1 18 1;
	setAttr -s 9 ".kix[4:8]"  1 1 0.80353242726805751 0.13508422587249769 
		0.13508422587249674;
	setAttr -s 9 ".kiy[4:8]"  0 0 0.59526098337511058 -0.99083411927548604 
		-0.99083411927548615;
	setAttr -s 9 ".kox[0:8]"  1 1 0.15717672547758932 1 1 0.80353242726805751 
		0.13508422587249763 0.13508422587249766 1;
	setAttr -s 9 ".koy[0:8]"  0 0 0.98757049215139192 0 0 0.59526098337511058 
		-0.99083411927548604 -0.99083411927548593 0;
createNode animCurveTA -n "CURVE11";
	rename -uid "41C00D9A-49DF-F759-1451-0D928114A90D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 9 ".ktv[0:8]"  141 0 157 0 162 0 167 -59.999999999999993
		 170 -59.999999999999993 187 -59.999999999999993 204 -59.999999999999993 206 -29.999999999999993
		 210 0;
	setAttr -s 9 ".kyts[7:8]" yes no;
	setAttr -s 9 ".kit[0:8]"  2 2 2 2 1 1 1 18 
		1;
	setAttr -s 9 ".kot[1:8]"  2 2 2 1 1 1 18 1;
	setAttr -s 9 ".kix[4:8]"  1 1 1 0.095060525440806884 0.095060525440806842;
	setAttr -s 9 ".kiy[4:8]"  0 0 0 0.99547149457074757 0.99547149457074757;
	setAttr -s 9 ".kox[0:8]"  1 1 0.079326696843658256 1 1 1 0.095060525440807439 
		0.09506052544080687 1;
	setAttr -s 9 ".koy[0:8]"  0 0 -0.99684867215032913 0 0 0 0.99547149457074746 
		0.99547149457074735 0;
createNode animCurveTU -n "CURVE12";
	rename -uid "DE46D074-43CD-E8F1-9529-3FA052E61531";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 6 ".ktv[0:5]"  141 1 157 1 162 1 167 1 187 1 206 1;
	setAttr -s 6 ".kyts[5]" yes;
	setAttr -s 6 ".kit[0:5]"  2 2 2 1 1 1;
	setAttr -s 6 ".kot[1:5]"  2 2 1 1 18;
	setAttr -s 6 ".kix[3:5]"  1 1 1;
	setAttr -s 6 ".kiy[3:5]"  0 0 0;
	setAttr -s 6 ".kox[0:5]"  1 1 1 1 1 1;
	setAttr -s 6 ".koy[0:5]"  0 0 0 0 0 0;
// End