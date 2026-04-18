//Maya ASCII 2022 scene
//Name: animation.ma
//Last modified: Fri, Jun 02, 2023 03:53:41 PM
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
fileInfo "UUID" "BE7C5C21-4078-4F54-84F6-B09775D71A66";
createNode animCurveTL -n "CURVE1";
	rename -uid "A98874A5-4BD3-5698-6E9E-2BA1C9AE729E";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 12 ".ktv[0:11]"  141 0 173 0 174 0 175 -5.9785318139667627
		 176 -9.5345231530376591 177 -13.617261576518883 178 -17.7 192 -17.7 195 0 217 0 221 0
		 281 0;
createNode animCurveTL -n "CURVE3";
	rename -uid "CE07918E-4E1C-BC1E-42AB-4197CE0DB52A";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 0.99023067773685369 270 0.99022109566312011;
createNode animCurveTL -n "CURVE4";
	rename -uid "E8EA0C32-4E8A-89EE-B35E-8FBF88F1014D";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 1.2298042375287278e-05 270 1.4877781140263091e-05;
createNode animCurveTL -n "CURVE5";
	rename -uid "8476109B-4B76-5959-21B8-6FA38DBBB150";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 -5.123206309136827 270 -5.1251175890888687;
createNode animCurveTU -n "CURVE6";
	rename -uid "2B2210FD-4E8D-22F6-04FF-BEA3A8F48171";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 0.99999999999999944 270 0.99999868869953346;
createNode animCurveTU -n "CURVE7";
	rename -uid "2B36F630-46C8-8690-2924-D6B3B328E8DA";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 1.0000000000000013 270 0.9999996423722608;
createNode animCurveTU -n "CURVE8";
	rename -uid "0C7BEA15-45F6-FBD6-0C0C-AA9C99E6AA78";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 1 270 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode animCurveTA -n "CURVE9";
	rename -uid "8C9487E9-4F24-D78D-93E5-9C90D9933075";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 -9.6602492616319774e-06 270 -179.98767634332808;
createNode animCurveTA -n "CURVE10";
	rename -uid "B5B61A19-43BE-35D5-D595-4782ACA26EA2";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 -6.0878359783950276e-06 270 179.99206333496141;
createNode animCurveTA -n "CURVE11";
	rename -uid "C27DF54B-4368-72B4-510B-9AB8DB0E8079";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 6.6669770834427846e-06 270 -179.99997807693305;
createNode animCurveTU -n "CURVE12";
	rename -uid "29ABD136-4011-0C7B-67A8-709DEFAD977A";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  0 0.99999999999999944 270 0.99999904632659187;
createNode animCurveTL -n "CURVE14";
	rename -uid "37A17356-499F-BE4E-3BF9-14A80C96B3A1";
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
createNode animCurveTL -n "CURVE15";
	rename -uid "B71F1625-4EC8-BB81-30CE-6DAEE35221D1";
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
createNode animCurveTL -n "CURVE16";
	rename -uid "E7A6086A-4973-8682-ADD9-D2AB736E09A7";
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
createNode animCurveTU -n "CURVE17";
	rename -uid "95B498D1-4984-6608-E0A3-76A36350917C";
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
createNode animCurveTU -n "CURVE18";
	rename -uid "92BF473E-4482-A1D1-77D4-C2A31B8174C5";
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
createNode animCurveTU -n "CURVE19";
	rename -uid "48BD1023-4459-6B21-5BFA-D9B8DA52FC6E";
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
createNode animCurveTA -n "CURVE20";
	rename -uid "EA261097-48BA-B595-74F2-F4BC82BCE033";
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
createNode animCurveTA -n "CURVE21";
	rename -uid "D18364A1-4DD6-8EA6-D45B-4DA9619B8979";
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
createNode animCurveTA -n "CURVE22";
	rename -uid "1F67763B-4076-5897-6607-48B5310320FD";
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
createNode animCurveTU -n "CURVE23";
	rename -uid "007E1089-4C58-59A7-CE4D-4D9011610351";
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