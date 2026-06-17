module exp_fixed_point (clk,
    enable,
    rst,
    exp_out,
    x_in);
 input clk;
 input enable;
 input rst;
 output [15:0] exp_out;
 input [7:0] x_in;

 wire _000_;
 wire _001_;
 wire _002_;
 wire _003_;
 wire _004_;
 wire _005_;
 wire _006_;
 wire _007_;
 wire _008_;
 wire _009_;
 wire _010_;
 wire _011_;
 wire _012_;
 wire _013_;
 wire _014_;
 wire _015_;
 wire _016_;
 wire _017_;
 wire _018_;
 wire clknet_1_0__leaf_clk;
 wire _020_;
 wire _021_;
 wire _022_;
 wire _023_;
 wire _024_;
 wire _025_;
 wire clknet_0_clk;
 wire net39;
 wire _028_;
 wire net36;
 wire _030_;
 wire net43;
 wire _032_;
 wire _033_;
 wire _034_;
 wire _035_;
 wire net42;
 wire net41;
 wire _038_;
 wire net40;
 wire _040_;
 wire _041_;
 wire _042_;
 wire net38;
 wire _044_;
 wire _045_;
 wire _046_;
 wire _047_;
 wire _048_;
 wire _049_;
 wire _050_;
 wire _051_;
 wire _052_;
 wire _053_;
 wire _054_;
 wire net37;
 wire net35;
 wire _057_;
 wire net34;
 wire _059_;
 wire _060_;
 wire _061_;
 wire _063_;
 wire _064_;
 wire _065_;
 wire _067_;
 wire _068_;
 wire _069_;
 wire _070_;
 wire _071_;
 wire _072_;
 wire _073_;
 wire _074_;
 wire _076_;
 wire _077_;
 wire _078_;
 wire _079_;
 wire _080_;
 wire _082_;
 wire _083_;
 wire _084_;
 wire _085_;
 wire _086_;
 wire _087_;
 wire _088_;
 wire _090_;
 wire _091_;
 wire _092_;
 wire _093_;
 wire _094_;
 wire _096_;
 wire _097_;
 wire _098_;
 wire _099_;
 wire _100_;
 wire _101_;
 wire _102_;
 wire _103_;
 wire _104_;
 wire _105_;
 wire _106_;
 wire _107_;
 wire _108_;
 wire _109_;
 wire _110_;
 wire _111_;
 wire _112_;
 wire _113_;
 wire _114_;
 wire _115_;
 wire _119_;
 wire _120_;
 wire _121_;
 wire _122_;
 wire _123_;
 wire _124_;
 wire _125_;
 wire _127_;
 wire _128_;
 wire _129_;
 wire _130_;
 wire _131_;
 wire _132_;
 wire _133_;
 wire _134_;
 wire _135_;
 wire _136_;
 wire _137_;
 wire _138_;
 wire _139_;
 wire _140_;
 wire _141_;
 wire _142_;
 wire _143_;
 wire _144_;
 wire _145_;
 wire _146_;
 wire _147_;
 wire _148_;
 wire _149_;
 wire _150_;
 wire _152_;
 wire _153_;
 wire _154_;
 wire _155_;
 wire _156_;
 wire _157_;
 wire _158_;
 wire _159_;
 wire _160_;
 wire _161_;
 wire _162_;
 wire _163_;
 wire _164_;
 wire _165_;
 wire _166_;
 wire _167_;
 wire _168_;
 wire _169_;
 wire _170_;
 wire _171_;
 wire _172_;
 wire _173_;
 wire _174_;
 wire _175_;
 wire _176_;
 wire _177_;
 wire _178_;
 wire _179_;
 wire _180_;
 wire _181_;
 wire _182_;
 wire _183_;
 wire _184_;
 wire _185_;
 wire _186_;
 wire _187_;
 wire _188_;
 wire _189_;
 wire _190_;
 wire _191_;
 wire _192_;
 wire _193_;
 wire _194_;
 wire _195_;
 wire _196_;
 wire _197_;
 wire _198_;
 wire _199_;
 wire _200_;
 wire _201_;
 wire _202_;
 wire _203_;
 wire _205_;
 wire _206_;
 wire _207_;
 wire _208_;
 wire _209_;
 wire _210_;
 wire _211_;
 wire _212_;
 wire _213_;
 wire _214_;
 wire _216_;
 wire _217_;
 wire _218_;
 wire _219_;
 wire _220_;
 wire _221_;
 wire _222_;
 wire _223_;
 wire _224_;
 wire _225_;
 wire _226_;
 wire _227_;
 wire _228_;
 wire _229_;
 wire _230_;
 wire _231_;
 wire _232_;
 wire _233_;
 wire _234_;
 wire _235_;
 wire _236_;
 wire _237_;
 wire _238_;
 wire _239_;
 wire _240_;
 wire _241_;
 wire _242_;
 wire _243_;
 wire _244_;
 wire _245_;
 wire _246_;
 wire _247_;
 wire _248_;
 wire _249_;
 wire _250_;
 wire _251_;
 wire _252_;
 wire _253_;
 wire _254_;
 wire _255_;
 wire _256_;
 wire _257_;
 wire _258_;
 wire _259_;
 wire _260_;
 wire _261_;
 wire _262_;
 wire _263_;
 wire _264_;
 wire _265_;
 wire _266_;
 wire _267_;
 wire _268_;
 wire _269_;
 wire _270_;
 wire _271_;
 wire _272_;
 wire _273_;
 wire _274_;
 wire _275_;
 wire _276_;
 wire _277_;
 wire _278_;
 wire _279_;
 wire _280_;
 wire _281_;
 wire _282_;
 wire _283_;
 wire _284_;
 wire _285_;
 wire _286_;
 wire _287_;
 wire _288_;
 wire _289_;
 wire _290_;
 wire _291_;
 wire _292_;
 wire _293_;
 wire _294_;
 wire _295_;
 wire _296_;
 wire _297_;
 wire _298_;
 wire _299_;
 wire _300_;
 wire _301_;
 wire _302_;
 wire _303_;
 wire _304_;
 wire _305_;
 wire _306_;
 wire _307_;
 wire _308_;
 wire _309_;
 wire _310_;
 wire _311_;
 wire _312_;
 wire _313_;
 wire _314_;
 wire _315_;
 wire _316_;
 wire _317_;
 wire _318_;
 wire _319_;
 wire _320_;
 wire _321_;
 wire _322_;
 wire _323_;
 wire _324_;
 wire _325_;
 wire _326_;
 wire _327_;
 wire _328_;
 wire _329_;
 wire _330_;
 wire _331_;
 wire _332_;
 wire _333_;
 wire _334_;
 wire _335_;
 wire _336_;
 wire _337_;
 wire _338_;
 wire _339_;
 wire _340_;
 wire _341_;
 wire _342_;
 wire _343_;
 wire _344_;
 wire _345_;
 wire _346_;
 wire _347_;
 wire _348_;
 wire _349_;
 wire _350_;
 wire _351_;
 wire _352_;
 wire _353_;
 wire _354_;
 wire _355_;
 wire _356_;
 wire _357_;
 wire _358_;
 wire _359_;
 wire _360_;
 wire _361_;
 wire _362_;
 wire _363_;
 wire _364_;
 wire _365_;
 wire _366_;
 wire _367_;
 wire _368_;
 wire _369_;
 wire _370_;
 wire _372_;
 wire _373_;
 wire _374_;
 wire _375_;
 wire _376_;
 wire _377_;
 wire _378_;
 wire _379_;
 wire _380_;
 wire _381_;
 wire _384_;
 wire _392_;
 wire _396_;
 wire _397_;
 wire _399_;
 wire _400_;
 wire _404_;
 wire _405_;
 wire _406_;
 wire _407_;
 wire _408_;
 wire _409_;
 wire _416_;
 wire _418_;
 wire _421_;
 wire _423_;
 wire _424_;
 wire _425_;
 wire _426_;
 wire clknet_1_1__leaf_clk;
 wire _429_;
 wire _430_;
 wire _431_;
 wire net6;
 wire net16;
 wire net17;
 wire net18;
 wire net19;
 wire net20;
 wire net21;
 wire net22;
 wire net23;
 wire net24;
 wire net25;
 wire net7;
 wire stage1_valid;
 wire \stage1_x[0] ;
 wire \stage1_x[1] ;
 wire \stage1_x[2] ;
 wire \stage1_x[3] ;
 wire \stage1_x[4] ;
 wire \stage1_x[5] ;
 wire \stage1_x[6] ;
 wire \stage1_x[7] ;
 wire net8;
 wire net9;
 wire net10;
 wire net11;
 wire net12;
 wire net13;
 wire net14;
 wire net15;

 sky130_fd_sc_hd__inv_1 _435_ (.A(\stage1_x[7] ),
    .Y(_384_));
 sky130_fd_sc_hd__nor2_1 _443_ (.A(\stage1_x[1] ),
    .B(net40),
    .Y(_392_));
 sky130_fd_sc_hd__nand2_2 _447_ (.A(net38),
    .B(net37),
    .Y(_396_));
 sky130_fd_sc_hd__nor2_1 _448_ (.A(_392_),
    .B(_396_),
    .Y(_397_));
 sky130_fd_sc_hd__o21ai_0 _450_ (.A1(net35),
    .A2(_397_),
    .B1(net34),
    .Y(_399_));
 sky130_fd_sc_hd__nand2_1 _451_ (.A(_384_),
    .B(_399_),
    .Y(_400_));
 sky130_fd_sc_hd__nand3_2 _455_ (.A(net38),
    .B(net37),
    .C(net35),
    .Y(_404_));
 sky130_fd_sc_hd__nand3_1 _456_ (.A(\stage1_x[7] ),
    .B(net34),
    .C(_404_),
    .Y(_405_));
 sky130_fd_sc_hd__inv_1 _457_ (.A(net34),
    .Y(_406_));
 sky130_fd_sc_hd__nand3_1 _458_ (.A(net35),
    .B(_406_),
    .C(_397_),
    .Y(_407_));
 sky130_fd_sc_hd__nand4_1 _459_ (.A(stage1_valid),
    .B(_400_),
    .C(_405_),
    .D(_407_),
    .Y(_408_));
 sky130_fd_sc_hd__nand2b_1 _460_ (.A_N(stage1_valid),
    .B(net24),
    .Y(_409_));
 sky130_fd_sc_hd__a21oi_1 _463_ (.A1(_408_),
    .A2(_409_),
    .B1(net43),
    .Y(_000_));
 sky130_fd_sc_hd__and2_0 _468_ (.A(\stage1_x[0] ),
    .B(net41),
    .X(_416_));
 sky130_fd_sc_hd__and2_0 _470_ (.A(\stage1_x[3] ),
    .B(net37),
    .X(_418_));
 sky130_fd_sc_hd__inv_1 _473_ (.A(net36),
    .Y(_421_));
 sky130_fd_sc_hd__o211ai_1 _475_ (.A1(net40),
    .A2(_416_),
    .B1(_418_),
    .C1(_421_),
    .Y(_423_));
 sky130_fd_sc_hd__nand2_1 _476_ (.A(net35),
    .B(_396_),
    .Y(_424_));
 sky130_fd_sc_hd__nand2_1 _477_ (.A(_423_),
    .B(_424_),
    .Y(_425_));
 sky130_fd_sc_hd__nor2_1 _478_ (.A(_392_),
    .B(_404_),
    .Y(_426_));
 sky130_fd_sc_hd__nor2_2 _481_ (.A(\stage1_x[0] ),
    .B(\stage1_x[1] ),
    .Y(_429_));
 sky130_fd_sc_hd__nor2_1 _482_ (.A(net40),
    .B(net38),
    .Y(_430_));
 sky130_fd_sc_hd__nand2_1 _483_ (.A(_429_),
    .B(_430_),
    .Y(_431_));
 sky130_fd_sc_hd__a21oi_1 _485_ (.A1(net37),
    .A2(_431_),
    .B1(net35),
    .Y(_020_));
 sky130_fd_sc_hd__nor3_1 _486_ (.A(net34),
    .B(_426_),
    .C(_020_),
    .Y(_021_));
 sky130_fd_sc_hd__a31oi_1 _487_ (.A1(\stage1_x[7] ),
    .A2(net34),
    .A3(_425_),
    .B1(_021_),
    .Y(_022_));
 sky130_fd_sc_hd__nor2_1 _488_ (.A(stage1_valid),
    .B(net23),
    .Y(_023_));
 sky130_fd_sc_hd__a311oi_1 _489_ (.A1(stage1_valid),
    .A2(_400_),
    .A3(_022_),
    .B1(_023_),
    .C1(net43),
    .Y(_001_));
 sky130_fd_sc_hd__nand2b_1 _490_ (.A_N(stage1_valid),
    .B(net22),
    .Y(_024_));
 sky130_fd_sc_hd__inv_2 _491_ (.A(net37),
    .Y(_025_));
 sky130_fd_sc_hd__o21a_1 _494_ (.A1(\stage1_x[0] ),
    .A2(net35),
    .B1(\stage1_x[1] ),
    .X(_028_));
 sky130_fd_sc_hd__o21ai_0 _496_ (.A1(net40),
    .A2(_028_),
    .B1(net38),
    .Y(_030_));
 sky130_fd_sc_hd__nand2_1 _498_ (.A(net42),
    .B(net41),
    .Y(_032_));
 sky130_fd_sc_hd__nor2_1 _499_ (.A(net40),
    .B(net36),
    .Y(_033_));
 sky130_fd_sc_hd__a21oi_1 _500_ (.A1(_032_),
    .A2(_033_),
    .B1(_396_),
    .Y(_034_));
 sky130_fd_sc_hd__a21oi_1 _501_ (.A1(_025_),
    .A2(_030_),
    .B1(_034_),
    .Y(_035_));
 sky130_fd_sc_hd__and2_1 _504_ (.A(\stage1_x[1] ),
    .B(net40),
    .X(_038_));
 sky130_fd_sc_hd__or2_1 _506_ (.A(net39),
    .B(net37),
    .X(_040_));
 sky130_fd_sc_hd__a21oi_1 _507_ (.A1(\stage1_x[0] ),
    .A2(_038_),
    .B1(_040_),
    .Y(_041_));
 sky130_fd_sc_hd__o21ai_0 _508_ (.A1(_397_),
    .A2(_041_),
    .B1(net35),
    .Y(_042_));
 sky130_fd_sc_hd__a31oi_1 _510_ (.A1(net37),
    .A2(_421_),
    .A3(_431_),
    .B1(net34),
    .Y(_044_));
 sky130_fd_sc_hd__a221o_1 _511_ (.A1(net34),
    .A2(_035_),
    .B1(_042_),
    .B2(_044_),
    .C1(_384_),
    .X(_045_));
 sky130_fd_sc_hd__a21boi_0 _512_ (.A1(_421_),
    .A2(_397_),
    .B1_N(_424_),
    .Y(_046_));
 sky130_fd_sc_hd__inv_1 _513_ (.A(net40),
    .Y(_047_));
 sky130_fd_sc_hd__clkinv_1 _514_ (.A(net39),
    .Y(_048_));
 sky130_fd_sc_hd__o21ai_0 _515_ (.A1(_047_),
    .A2(_429_),
    .B1(_048_),
    .Y(_049_));
 sky130_fd_sc_hd__nand2_1 _516_ (.A(net37),
    .B(net36),
    .Y(_050_));
 sky130_fd_sc_hd__nor2_1 _517_ (.A(net34),
    .B(_050_),
    .Y(_051_));
 sky130_fd_sc_hd__a221o_1 _518_ (.A1(net34),
    .A2(_046_),
    .B1(_049_),
    .B2(_051_),
    .C1(\stage1_x[7] ),
    .X(_052_));
 sky130_fd_sc_hd__nand3_1 _519_ (.A(stage1_valid),
    .B(_045_),
    .C(_052_),
    .Y(_053_));
 sky130_fd_sc_hd__a21oi_1 _520_ (.A1(_024_),
    .A2(_053_),
    .B1(net43),
    .Y(_002_));
 sky130_fd_sc_hd__nand2b_1 _521_ (.A_N(stage1_valid),
    .B(net21),
    .Y(_054_));
 sky130_fd_sc_hd__nor2_1 _524_ (.A(net37),
    .B(_429_),
    .Y(_057_));
 sky130_fd_sc_hd__o21ai_0 _526_ (.A1(\stage1_x[3] ),
    .A2(_416_),
    .B1(net35),
    .Y(_059_));
 sky130_fd_sc_hd__o21ai_0 _527_ (.A1(\stage1_x[3] ),
    .A2(_057_),
    .B1(_059_),
    .Y(_060_));
 sky130_fd_sc_hd__and2_1 _528_ (.A(net37),
    .B(net36),
    .X(_061_));
 sky130_fd_sc_hd__nor2_1 _530_ (.A(net37),
    .B(net36),
    .Y(_063_));
 sky130_fd_sc_hd__a221oi_1 _531_ (.A1(_392_),
    .A2(_061_),
    .B1(_063_),
    .B2(\stage1_x[3] ),
    .C1(net34),
    .Y(_064_));
 sky130_fd_sc_hd__o21ai_0 _532_ (.A1(_047_),
    .A2(_060_),
    .B1(_064_),
    .Y(_065_));
 sky130_fd_sc_hd__nand2b_1 _534_ (.A_N(net40),
    .B(net37),
    .Y(_067_));
 sky130_fd_sc_hd__nor2_1 _535_ (.A(net41),
    .B(_067_),
    .Y(_068_));
 sky130_fd_sc_hd__clkinv_1 _536_ (.A(\stage1_x[0] ),
    .Y(_069_));
 sky130_fd_sc_hd__o21ai_0 _537_ (.A1(net35),
    .A2(_068_),
    .B1(_069_),
    .Y(_070_));
 sky130_fd_sc_hd__nand2b_2 _538_ (.A_N(net37),
    .B(net40),
    .Y(_071_));
 sky130_fd_sc_hd__nand2_1 _539_ (.A(net36),
    .B(_071_),
    .Y(_072_));
 sky130_fd_sc_hd__a21oi_1 _540_ (.A1(_070_),
    .A2(_072_),
    .B1(\stage1_x[3] ),
    .Y(_073_));
 sky130_fd_sc_hd__nand2b_1 _541_ (.A_N(net40),
    .B(\stage1_x[3] ),
    .Y(_074_));
 sky130_fd_sc_hd__nor2_1 _543_ (.A(\stage1_x[0] ),
    .B(net40),
    .Y(_076_));
 sky130_fd_sc_hd__o21bai_1 _544_ (.A1(net39),
    .A2(_076_),
    .B1_N(net41),
    .Y(_077_));
 sky130_fd_sc_hd__a31oi_1 _545_ (.A1(_061_),
    .A2(_074_),
    .A3(_077_),
    .B1(_406_),
    .Y(_078_));
 sky130_fd_sc_hd__nor2_1 _546_ (.A(net39),
    .B(net37),
    .Y(_079_));
 sky130_fd_sc_hd__nor2b_1 _547_ (.A(net35),
    .B_N(\stage1_x[3] ),
    .Y(_080_));
 sky130_fd_sc_hd__nand2b_1 _549_ (.A_N(\stage1_x[3] ),
    .B(net40),
    .Y(_082_));
 sky130_fd_sc_hd__o21ai_0 _550_ (.A1(net41),
    .A2(_074_),
    .B1(_082_),
    .Y(_083_));
 sky130_fd_sc_hd__a222oi_1 _551_ (.A1(_416_),
    .A2(_079_),
    .B1(_076_),
    .B2(_080_),
    .C1(_083_),
    .C2(_050_),
    .Y(_084_));
 sky130_fd_sc_hd__nand2_1 _552_ (.A(\stage1_x[7] ),
    .B(stage1_valid),
    .Y(_085_));
 sky130_fd_sc_hd__a21oi_1 _553_ (.A1(_078_),
    .A2(_084_),
    .B1(_085_),
    .Y(_086_));
 sky130_fd_sc_hd__o21ai_0 _554_ (.A1(_065_),
    .A2(_073_),
    .B1(_086_),
    .Y(_087_));
 sky130_fd_sc_hd__or2_0 _555_ (.A(\stage1_x[1] ),
    .B(net40),
    .X(_088_));
 sky130_fd_sc_hd__o21ai_0 _557_ (.A1(\stage1_x[0] ),
    .A2(_088_),
    .B1(\stage1_x[3] ),
    .Y(_090_));
 sky130_fd_sc_hd__nand2_1 _558_ (.A(net37),
    .B(_088_),
    .Y(_091_));
 sky130_fd_sc_hd__o21ai_0 _559_ (.A1(_421_),
    .A2(_088_),
    .B1(_091_),
    .Y(_092_));
 sky130_fd_sc_hd__a22o_1 _560_ (.A1(_025_),
    .A2(_090_),
    .B1(_092_),
    .B2(\stage1_x[3] ),
    .X(_093_));
 sky130_fd_sc_hd__nand2b_1 _561_ (.A_N(net36),
    .B(net37),
    .Y(_094_));
 sky130_fd_sc_hd__nand2_1 _563_ (.A(net40),
    .B(net38),
    .Y(_096_));
 sky130_fd_sc_hd__nor3_1 _564_ (.A(_429_),
    .B(_094_),
    .C(_096_),
    .Y(_097_));
 sky130_fd_sc_hd__a21oi_1 _565_ (.A1(net37),
    .A2(_049_),
    .B1(_421_),
    .Y(_098_));
 sky130_fd_sc_hd__nor3_1 _566_ (.A(net34),
    .B(_097_),
    .C(_098_),
    .Y(_099_));
 sky130_fd_sc_hd__nand2_1 _567_ (.A(_384_),
    .B(stage1_valid),
    .Y(_100_));
 sky130_fd_sc_hd__a211o_1 _568_ (.A1(net34),
    .A2(_093_),
    .B1(_099_),
    .C1(_100_),
    .X(_101_));
 sky130_fd_sc_hd__a31oi_1 _569_ (.A1(_054_),
    .A2(_087_),
    .A3(_101_),
    .B1(net43),
    .Y(_003_));
 sky130_fd_sc_hd__nor3b_1 _570_ (.A(net37),
    .B(net36),
    .C_N(\stage1_x[0] ),
    .Y(_102_));
 sky130_fd_sc_hd__o21ai_0 _571_ (.A1(_088_),
    .A2(_102_),
    .B1(\stage1_x[3] ),
    .Y(_103_));
 sky130_fd_sc_hd__o311ai_0 _572_ (.A1(\stage1_x[3] ),
    .A2(_088_),
    .A3(_063_),
    .B1(_103_),
    .C1(_050_),
    .Y(_104_));
 sky130_fd_sc_hd__a21oi_1 _573_ (.A1(_078_),
    .A2(_104_),
    .B1(_100_),
    .Y(_105_));
 sky130_fd_sc_hd__and2_0 _574_ (.A(net40),
    .B(net39),
    .X(_106_));
 sky130_fd_sc_hd__nand2_1 _575_ (.A(_416_),
    .B(_106_),
    .Y(_107_));
 sky130_fd_sc_hd__a21o_1 _576_ (.A1(_049_),
    .A2(_107_),
    .B1(_050_),
    .X(_108_));
 sky130_fd_sc_hd__nor2b_1 _577_ (.A(net37),
    .B_N(\stage1_x[3] ),
    .Y(_109_));
 sky130_fd_sc_hd__or2_1 _578_ (.A(\stage1_x[0] ),
    .B(\stage1_x[1] ),
    .X(_110_));
 sky130_fd_sc_hd__a21oi_1 _579_ (.A1(_110_),
    .A2(_106_),
    .B1(_094_),
    .Y(_111_));
 sky130_fd_sc_hd__a31oi_1 _580_ (.A1(net35),
    .A2(_088_),
    .A3(_109_),
    .B1(_111_),
    .Y(_112_));
 sky130_fd_sc_hd__nand3_1 _581_ (.A(_406_),
    .B(_108_),
    .C(_112_),
    .Y(_113_));
 sky130_fd_sc_hd__nor2b_1 _582_ (.A(stage1_valid),
    .B_N(net20),
    .Y(_114_));
 sky130_fd_sc_hd__a21oi_1 _583_ (.A1(_105_),
    .A2(_113_),
    .B1(_114_),
    .Y(_115_));
 sky130_fd_sc_hd__o21ai_0 _587_ (.A1(net42),
    .A2(net41),
    .B1(_079_),
    .Y(_119_));
 sky130_fd_sc_hd__a21oi_1 _588_ (.A1(_416_),
    .A2(_080_),
    .B1(net40),
    .Y(_120_));
 sky130_fd_sc_hd__nand2_1 _589_ (.A(net42),
    .B(_048_),
    .Y(_121_));
 sky130_fd_sc_hd__and2_1 _590_ (.A(net41),
    .B(net36),
    .X(_122_));
 sky130_fd_sc_hd__a211oi_1 _591_ (.A1(_121_),
    .A2(_122_),
    .B1(_047_),
    .C1(_109_),
    .Y(_123_));
 sky130_fd_sc_hd__a21oi_1 _592_ (.A1(_119_),
    .A2(_120_),
    .B1(_123_),
    .Y(_124_));
 sky130_fd_sc_hd__or2_0 _593_ (.A(net40),
    .B(net38),
    .X(_125_));
 sky130_fd_sc_hd__o21ai_0 _595_ (.A1(net36),
    .A2(_125_),
    .B1(_071_),
    .Y(_127_));
 sky130_fd_sc_hd__nand2_1 _596_ (.A(\stage1_x[0] ),
    .B(net36),
    .Y(_128_));
 sky130_fd_sc_hd__o22ai_1 _597_ (.A1(net40),
    .A2(_396_),
    .B1(_082_),
    .B2(_128_),
    .Y(_129_));
 sky130_fd_sc_hd__a21oi_1 _598_ (.A1(_069_),
    .A2(_127_),
    .B1(_129_),
    .Y(_130_));
 sky130_fd_sc_hd__o22ai_1 _599_ (.A1(net36),
    .A2(_074_),
    .B1(_082_),
    .B2(_032_),
    .Y(_131_));
 sky130_fd_sc_hd__a21oi_1 _600_ (.A1(net37),
    .A2(_131_),
    .B1(net34),
    .Y(_132_));
 sky130_fd_sc_hd__o21ai_0 _601_ (.A1(net41),
    .A2(_130_),
    .B1(_132_),
    .Y(_133_));
 sky130_fd_sc_hd__nor2_1 _602_ (.A(_124_),
    .B(_133_),
    .Y(_134_));
 sky130_fd_sc_hd__a21oi_1 _603_ (.A1(\stage1_x[1] ),
    .A2(net37),
    .B1(\stage1_x[3] ),
    .Y(_135_));
 sky130_fd_sc_hd__o21ai_0 _604_ (.A1(_421_),
    .A2(_135_),
    .B1(_069_),
    .Y(_136_));
 sky130_fd_sc_hd__and2_1 _605_ (.A(\stage1_x[1] ),
    .B(\stage1_x[3] ),
    .X(_137_));
 sky130_fd_sc_hd__a21oi_1 _606_ (.A1(net37),
    .A2(net36),
    .B1(\stage1_x[1] ),
    .Y(_138_));
 sky130_fd_sc_hd__a21oi_1 _607_ (.A1(_061_),
    .A2(_137_),
    .B1(_138_),
    .Y(_139_));
 sky130_fd_sc_hd__nand2_1 _608_ (.A(_136_),
    .B(_139_),
    .Y(_140_));
 sky130_fd_sc_hd__o21ai_0 _609_ (.A1(_421_),
    .A2(_135_),
    .B1(_076_),
    .Y(_141_));
 sky130_fd_sc_hd__o21ai_0 _610_ (.A1(_047_),
    .A2(_140_),
    .B1(_141_),
    .Y(_142_));
 sky130_fd_sc_hd__a31oi_1 _611_ (.A1(\stage1_x[0] ),
    .A2(_061_),
    .A3(_137_),
    .B1(_138_),
    .Y(_143_));
 sky130_fd_sc_hd__nor3b_1 _612_ (.A(\stage1_x[3] ),
    .B(net35),
    .C_N(net37),
    .Y(_144_));
 sky130_fd_sc_hd__nand2_1 _613_ (.A(_416_),
    .B(_144_),
    .Y(_145_));
 sky130_fd_sc_hd__o211ai_1 _614_ (.A1(net40),
    .A2(_143_),
    .B1(_145_),
    .C1(net34),
    .Y(_146_));
 sky130_fd_sc_hd__nor2_1 _615_ (.A(net43),
    .B(_085_),
    .Y(_147_));
 sky130_fd_sc_hd__o21ai_0 _616_ (.A1(_142_),
    .A2(_146_),
    .B1(_147_),
    .Y(_148_));
 sky130_fd_sc_hd__o22ai_1 _617_ (.A1(net43),
    .A2(_115_),
    .B1(_134_),
    .B2(_148_),
    .Y(_004_));
 sky130_fd_sc_hd__xnor2_1 _618_ (.A(net38),
    .B(_033_),
    .Y(_149_));
 sky130_fd_sc_hd__a2bb2oi_1 _619_ (.A1_N(_421_),
    .A2_N(_071_),
    .B1(_080_),
    .B2(_047_),
    .Y(_150_));
 sky130_fd_sc_hd__o22ai_1 _621_ (.A1(net37),
    .A2(_149_),
    .B1(_150_),
    .B2(net42),
    .Y(_152_));
 sky130_fd_sc_hd__a21oi_1 _622_ (.A1(net36),
    .A2(_430_),
    .B1(_080_),
    .Y(_153_));
 sky130_fd_sc_hd__nor3_1 _623_ (.A(_025_),
    .B(_032_),
    .C(_153_),
    .Y(_154_));
 sky130_fd_sc_hd__nor2_1 _624_ (.A(net42),
    .B(_047_),
    .Y(_155_));
 sky130_fd_sc_hd__a21boi_0 _625_ (.A1(net41),
    .A2(_094_),
    .B1_N(_155_),
    .Y(_156_));
 sky130_fd_sc_hd__nand2b_1 _626_ (.A_N(net37),
    .B(net36),
    .Y(_157_));
 sky130_fd_sc_hd__a221oi_1 _627_ (.A1(net42),
    .A2(_047_),
    .B1(_094_),
    .B2(_157_),
    .C1(net41),
    .Y(_158_));
 sky130_fd_sc_hd__a21oi_1 _628_ (.A1(net42),
    .A2(_047_),
    .B1(_061_),
    .Y(_159_));
 sky130_fd_sc_hd__nand2_1 _629_ (.A(_063_),
    .B(_076_),
    .Y(_160_));
 sky130_fd_sc_hd__o211ai_1 _630_ (.A1(net41),
    .A2(_159_),
    .B1(_160_),
    .C1(net39),
    .Y(_161_));
 sky130_fd_sc_hd__o31a_1 _631_ (.A1(\stage1_x[3] ),
    .A2(_156_),
    .A3(_158_),
    .B1(_161_),
    .X(_162_));
 sky130_fd_sc_hd__a2111oi_1 _632_ (.A1(net41),
    .A2(_152_),
    .B1(_154_),
    .C1(net34),
    .D1(_162_),
    .Y(_163_));
 sky130_fd_sc_hd__nand2_1 _633_ (.A(net39),
    .B(_025_),
    .Y(_164_));
 sky130_fd_sc_hd__nand2b_1 _634_ (.A_N(\stage1_x[1] ),
    .B(net36),
    .Y(_165_));
 sky130_fd_sc_hd__o22ai_1 _635_ (.A1(\stage1_x[1] ),
    .A2(net36),
    .B1(_157_),
    .B2(_048_),
    .Y(_166_));
 sky130_fd_sc_hd__nand2_1 _636_ (.A(\stage1_x[1] ),
    .B(net37),
    .Y(_167_));
 sky130_fd_sc_hd__nor2b_1 _637_ (.A(net36),
    .B_N(net40),
    .Y(_168_));
 sky130_fd_sc_hd__nor3_1 _638_ (.A(net39),
    .B(_167_),
    .C(_168_),
    .Y(_169_));
 sky130_fd_sc_hd__nand2_1 _639_ (.A(net39),
    .B(net36),
    .Y(_170_));
 sky130_fd_sc_hd__a21oi_1 _640_ (.A1(net37),
    .A2(_170_),
    .B1(\stage1_x[1] ),
    .Y(_171_));
 sky130_fd_sc_hd__a211oi_1 _641_ (.A1(net40),
    .A2(_166_),
    .B1(_169_),
    .C1(_171_),
    .Y(_172_));
 sky130_fd_sc_hd__o2111ai_1 _642_ (.A1(_164_),
    .A2(_165_),
    .B1(_172_),
    .C1(net34),
    .D1(\stage1_x[0] ),
    .Y(_173_));
 sky130_fd_sc_hd__nand2_1 _643_ (.A(_048_),
    .B(net37),
    .Y(_174_));
 sky130_fd_sc_hd__a21oi_1 _644_ (.A1(_164_),
    .A2(_174_),
    .B1(_165_),
    .Y(_175_));
 sky130_fd_sc_hd__nor2b_1 _645_ (.A(net40),
    .B_N(net37),
    .Y(_176_));
 sky130_fd_sc_hd__o21ai_0 _646_ (.A1(\stage1_x[3] ),
    .A2(_176_),
    .B1(net36),
    .Y(_177_));
 sky130_fd_sc_hd__nor3_1 _647_ (.A(\stage1_x[3] ),
    .B(net37),
    .C(net36),
    .Y(_178_));
 sky130_fd_sc_hd__a21oi_1 _648_ (.A1(\stage1_x[1] ),
    .A2(_418_),
    .B1(_178_),
    .Y(_179_));
 sky130_fd_sc_hd__o2bb2ai_1 _649_ (.A1_N(\stage1_x[1] ),
    .A2_N(_177_),
    .B1(_179_),
    .B2(net40),
    .Y(_180_));
 sky130_fd_sc_hd__or4_1 _650_ (.A(\stage1_x[0] ),
    .B(_406_),
    .C(_175_),
    .D(_180_),
    .X(_181_));
 sky130_fd_sc_hd__nand3_1 _651_ (.A(_147_),
    .B(_173_),
    .C(_181_),
    .Y(_182_));
 sky130_fd_sc_hd__nor2b_1 _652_ (.A(\stage1_x[0] ),
    .B_N(net36),
    .Y(_183_));
 sky130_fd_sc_hd__nor2_1 _653_ (.A(_047_),
    .B(_183_),
    .Y(_184_));
 sky130_fd_sc_hd__nor2_1 _654_ (.A(net41),
    .B(net37),
    .Y(_185_));
 sky130_fd_sc_hd__o21ai_0 _655_ (.A1(_421_),
    .A2(_185_),
    .B1(_047_),
    .Y(_186_));
 sky130_fd_sc_hd__inv_1 _656_ (.A(_063_),
    .Y(_187_));
 sky130_fd_sc_hd__o211ai_1 _657_ (.A1(_167_),
    .A2(_184_),
    .B1(_186_),
    .C1(_187_),
    .Y(_188_));
 sky130_fd_sc_hd__nand3_1 _658_ (.A(_048_),
    .B(_025_),
    .C(net36),
    .Y(_189_));
 sky130_fd_sc_hd__o21ai_1 _659_ (.A1(_109_),
    .A2(_144_),
    .B1(_416_),
    .Y(_190_));
 sky130_fd_sc_hd__mux2i_1 _660_ (.A0(net35),
    .A1(net37),
    .S(net38),
    .Y(_191_));
 sky130_fd_sc_hd__o22a_1 _661_ (.A1(\stage1_x[1] ),
    .A2(_404_),
    .B1(_110_),
    .B2(_191_),
    .X(_192_));
 sky130_fd_sc_hd__a31oi_1 _662_ (.A1(_189_),
    .A2(_190_),
    .A3(_192_),
    .B1(_047_),
    .Y(_193_));
 sky130_fd_sc_hd__a221oi_1 _663_ (.A1(_061_),
    .A2(_430_),
    .B1(_188_),
    .B2(net38),
    .C1(_193_),
    .Y(_194_));
 sky130_fd_sc_hd__nand2b_1 _664_ (.A_N(\stage1_x[1] ),
    .B(net40),
    .Y(_195_));
 sky130_fd_sc_hd__o2111ai_1 _665_ (.A1(_094_),
    .A2(_195_),
    .B1(_384_),
    .C1(stage1_valid),
    .D1(net34),
    .Y(_196_));
 sky130_fd_sc_hd__a31oi_1 _666_ (.A1(_429_),
    .A2(_063_),
    .A3(_106_),
    .B1(_196_),
    .Y(_197_));
 sky130_fd_sc_hd__nor2b_1 _667_ (.A(\stage1_x[0] ),
    .B_N(net38),
    .Y(_198_));
 sky130_fd_sc_hd__nor2_1 _668_ (.A(net37),
    .B(_198_),
    .Y(_199_));
 sky130_fd_sc_hd__o21ai_0 _669_ (.A1(net41),
    .A2(_199_),
    .B1(_033_),
    .Y(_200_));
 sky130_fd_sc_hd__nand2b_1 _670_ (.A_N(stage1_valid),
    .B(net19),
    .Y(_201_));
 sky130_fd_sc_hd__a21boi_0 _671_ (.A1(_197_),
    .A2(_200_),
    .B1_N(_201_),
    .Y(_202_));
 sky130_fd_sc_hd__nand2b_1 _672_ (.A_N(net40),
    .B(\stage1_x[1] ),
    .Y(_203_));
 sky130_fd_sc_hd__nor2b_1 _674_ (.A(\stage1_x[1] ),
    .B_N(net40),
    .Y(_205_));
 sky130_fd_sc_hd__nand3_1 _675_ (.A(_069_),
    .B(_396_),
    .C(_205_),
    .Y(_206_));
 sky130_fd_sc_hd__o221ai_1 _676_ (.A1(_040_),
    .A2(_195_),
    .B1(_203_),
    .B2(_418_),
    .C1(_206_),
    .Y(_207_));
 sky130_fd_sc_hd__nand2_1 _677_ (.A(net41),
    .B(net40),
    .Y(_208_));
 sky130_fd_sc_hd__nand2b_1 _678_ (.A_N(net41),
    .B(net42),
    .Y(_209_));
 sky130_fd_sc_hd__nor2b_1 _679_ (.A(_198_),
    .B_N(_209_),
    .Y(_210_));
 sky130_fd_sc_hd__o22ai_1 _680_ (.A1(_396_),
    .A2(_208_),
    .B1(_067_),
    .B2(_210_),
    .Y(_211_));
 sky130_fd_sc_hd__o211a_1 _681_ (.A1(_207_),
    .A2(_211_),
    .B1(net35),
    .C1(_201_),
    .X(_212_));
 sky130_fd_sc_hd__o32a_1 _682_ (.A1(net34),
    .A2(_100_),
    .A3(_194_),
    .B1(_202_),
    .B2(_212_),
    .X(_213_));
 sky130_fd_sc_hd__o22ai_1 _683_ (.A1(_163_),
    .A2(_182_),
    .B1(_213_),
    .B2(net43),
    .Y(_005_));
 sky130_fd_sc_hd__inv_1 _684_ (.A(net18),
    .Y(_214_));
 sky130_fd_sc_hd__or2_1 _686_ (.A(net41),
    .B(net38),
    .X(_216_));
 sky130_fd_sc_hd__and2b_1 _687_ (.A_N(net38),
    .B(net41),
    .X(_217_));
 sky130_fd_sc_hd__nor3_1 _688_ (.A(net42),
    .B(_217_),
    .C(_185_),
    .Y(_218_));
 sky130_fd_sc_hd__a31oi_1 _689_ (.A1(net42),
    .A2(_167_),
    .A3(_216_),
    .B1(_218_),
    .Y(_219_));
 sky130_fd_sc_hd__nand2_1 _690_ (.A(\stage1_x[1] ),
    .B(net38),
    .Y(_220_));
 sky130_fd_sc_hd__nor2b_1 _691_ (.A(net38),
    .B_N(net37),
    .Y(_221_));
 sky130_fd_sc_hd__a21oi_1 _692_ (.A1(_392_),
    .A2(_221_),
    .B1(_033_),
    .Y(_222_));
 sky130_fd_sc_hd__o211ai_1 _693_ (.A1(_220_),
    .A2(_155_),
    .B1(_222_),
    .C1(_094_),
    .Y(_223_));
 sky130_fd_sc_hd__a21oi_1 _694_ (.A1(net40),
    .A2(_219_),
    .B1(_223_),
    .Y(_224_));
 sky130_fd_sc_hd__o211ai_1 _695_ (.A1(net42),
    .A2(_137_),
    .B1(_216_),
    .C1(net37),
    .Y(_225_));
 sky130_fd_sc_hd__a211oi_1 _696_ (.A1(_069_),
    .A2(_048_),
    .B1(_167_),
    .C1(net40),
    .Y(_226_));
 sky130_fd_sc_hd__a21oi_1 _697_ (.A1(net40),
    .A2(_225_),
    .B1(_226_),
    .Y(_227_));
 sky130_fd_sc_hd__nor2_1 _698_ (.A(net35),
    .B(_227_),
    .Y(_228_));
 sky130_fd_sc_hd__nor2_1 _699_ (.A(net43),
    .B(_100_),
    .Y(_229_));
 sky130_fd_sc_hd__o21ai_0 _700_ (.A1(net42),
    .A2(_203_),
    .B1(_209_),
    .Y(_230_));
 sky130_fd_sc_hd__xnor2_1 _701_ (.A(_048_),
    .B(_230_),
    .Y(_231_));
 sky130_fd_sc_hd__nor2b_1 _702_ (.A(net37),
    .B_N(net41),
    .Y(_232_));
 sky130_fd_sc_hd__o221ai_1 _703_ (.A1(net42),
    .A2(_048_),
    .B1(_421_),
    .B2(_106_),
    .C1(_232_),
    .Y(_233_));
 sky130_fd_sc_hd__nor2_1 _704_ (.A(_096_),
    .B(_128_),
    .Y(_234_));
 sky130_fd_sc_hd__or4b_1 _705_ (.A(_102_),
    .B(_178_),
    .C(_234_),
    .D_N(_138_),
    .X(_235_));
 sky130_fd_sc_hd__o2111ai_1 _706_ (.A1(_050_),
    .A2(_231_),
    .B1(_233_),
    .C1(net34),
    .D1(_235_),
    .Y(_236_));
 sky130_fd_sc_hd__o311ai_1 _707_ (.A1(net34),
    .A2(_224_),
    .A3(_228_),
    .B1(_229_),
    .C1(_236_),
    .Y(_237_));
 sky130_fd_sc_hd__nor2_1 _708_ (.A(net40),
    .B(net37),
    .Y(_238_));
 sky130_fd_sc_hd__nor2_1 _709_ (.A(_221_),
    .B(_238_),
    .Y(_239_));
 sky130_fd_sc_hd__o22ai_1 _710_ (.A1(net40),
    .A2(_174_),
    .B1(_239_),
    .B2(\stage1_x[1] ),
    .Y(_240_));
 sky130_fd_sc_hd__a21o_1 _711_ (.A1(_067_),
    .A2(_071_),
    .B1(net41),
    .X(_241_));
 sky130_fd_sc_hd__o21ai_0 _712_ (.A1(net38),
    .A2(_238_),
    .B1(\stage1_x[1] ),
    .Y(_242_));
 sky130_fd_sc_hd__a31oi_1 _713_ (.A1(_096_),
    .A2(_241_),
    .A3(_242_),
    .B1(net42),
    .Y(_243_));
 sky130_fd_sc_hd__a21oi_1 _714_ (.A1(net42),
    .A2(_079_),
    .B1(_418_),
    .Y(_244_));
 sky130_fd_sc_hd__o21ai_0 _715_ (.A1(_208_),
    .A2(_244_),
    .B1(net36),
    .Y(_245_));
 sky130_fd_sc_hd__a211oi_1 _716_ (.A1(net42),
    .A2(_240_),
    .B1(_243_),
    .C1(_245_),
    .Y(_246_));
 sky130_fd_sc_hd__nand2_1 _717_ (.A(_195_),
    .B(_203_),
    .Y(_247_));
 sky130_fd_sc_hd__nor2b_1 _718_ (.A(net40),
    .B_N(net38),
    .Y(_248_));
 sky130_fd_sc_hd__a211oi_1 _719_ (.A1(\stage1_x[1] ),
    .A2(_248_),
    .B1(_205_),
    .C1(\stage1_x[0] ),
    .Y(_249_));
 sky130_fd_sc_hd__a21oi_1 _720_ (.A1(\stage1_x[0] ),
    .A2(_247_),
    .B1(_249_),
    .Y(_250_));
 sky130_fd_sc_hd__nand2_1 _721_ (.A(net38),
    .B(_203_),
    .Y(_251_));
 sky130_fd_sc_hd__nand2_1 _722_ (.A(\stage1_x[1] ),
    .B(_430_),
    .Y(_252_));
 sky130_fd_sc_hd__nand3_1 _723_ (.A(_069_),
    .B(_251_),
    .C(_252_),
    .Y(_253_));
 sky130_fd_sc_hd__nor2_1 _724_ (.A(\stage1_x[1] ),
    .B(net38),
    .Y(_254_));
 sky130_fd_sc_hd__nand2_1 _725_ (.A(net40),
    .B(_254_),
    .Y(_255_));
 sky130_fd_sc_hd__a31oi_1 _726_ (.A1(\stage1_x[0] ),
    .A2(_220_),
    .A3(_255_),
    .B1(net37),
    .Y(_256_));
 sky130_fd_sc_hd__a221oi_1 _727_ (.A1(net37),
    .A2(_250_),
    .B1(_253_),
    .B2(_256_),
    .C1(net35),
    .Y(_257_));
 sky130_fd_sc_hd__nor2_1 _728_ (.A(_176_),
    .B(_198_),
    .Y(_258_));
 sky130_fd_sc_hd__a21o_1 _729_ (.A1(_396_),
    .A2(_203_),
    .B1(\stage1_x[0] ),
    .X(_259_));
 sky130_fd_sc_hd__o221ai_1 _730_ (.A1(net40),
    .A2(_174_),
    .B1(_258_),
    .B2(\stage1_x[1] ),
    .C1(_259_),
    .Y(_260_));
 sky130_fd_sc_hd__a21bo_1 _731_ (.A1(\stage1_x[1] ),
    .A2(net40),
    .B1_N(net39),
    .X(_261_));
 sky130_fd_sc_hd__nor2b_2 _732_ (.A(net38),
    .B_N(net40),
    .Y(_262_));
 sky130_fd_sc_hd__a32oi_1 _733_ (.A1(\stage1_x[1] ),
    .A2(net36),
    .A3(_262_),
    .B1(_183_),
    .B2(_261_),
    .Y(_263_));
 sky130_fd_sc_hd__o221ai_1 _734_ (.A1(\stage1_x[0] ),
    .A2(_082_),
    .B1(_128_),
    .B2(_261_),
    .C1(_263_),
    .Y(_264_));
 sky130_fd_sc_hd__o21ai_0 _735_ (.A1(net42),
    .A2(_208_),
    .B1(_061_),
    .Y(_265_));
 sky130_fd_sc_hd__nor2b_1 _736_ (.A(\stage1_x[1] ),
    .B_N(net39),
    .Y(_266_));
 sky130_fd_sc_hd__maj3_1 _737_ (.A(\stage1_x[0] ),
    .B(_047_),
    .C(_266_),
    .X(_267_));
 sky130_fd_sc_hd__o21ai_0 _738_ (.A1(_265_),
    .A2(_267_),
    .B1(net34),
    .Y(_268_));
 sky130_fd_sc_hd__a221o_1 _739_ (.A1(_421_),
    .A2(_260_),
    .B1(_264_),
    .B2(_025_),
    .C1(_268_),
    .X(_269_));
 sky130_fd_sc_hd__nor2_1 _740_ (.A(_384_),
    .B(net43),
    .Y(_270_));
 sky130_fd_sc_hd__o21a_1 _741_ (.A1(stage1_valid),
    .A2(net18),
    .B1(_270_),
    .X(_271_));
 sky130_fd_sc_hd__o311ai_1 _742_ (.A1(net34),
    .A2(_246_),
    .A3(_257_),
    .B1(_269_),
    .C1(_271_),
    .Y(_272_));
 sky130_fd_sc_hd__o311ai_1 _743_ (.A1(stage1_valid),
    .A2(_214_),
    .A3(net43),
    .B1(_237_),
    .C1(_272_),
    .Y(_006_));
 sky130_fd_sc_hd__nor2b_1 _744_ (.A(net40),
    .B_N(net36),
    .Y(_273_));
 sky130_fd_sc_hd__nor3_1 _745_ (.A(_069_),
    .B(net37),
    .C(_273_),
    .Y(_274_));
 sky130_fd_sc_hd__nor2_1 _746_ (.A(\stage1_x[0] ),
    .B(_025_),
    .Y(_275_));
 sky130_fd_sc_hd__o21ai_0 _747_ (.A1(_274_),
    .A2(_275_),
    .B1(net38),
    .Y(_276_));
 sky130_fd_sc_hd__a21oi_1 _748_ (.A1(net36),
    .A2(_208_),
    .B1(_262_),
    .Y(_277_));
 sky130_fd_sc_hd__o22ai_1 _749_ (.A1(net42),
    .A2(net38),
    .B1(net36),
    .B2(_071_),
    .Y(_278_));
 sky130_fd_sc_hd__a2bb2oi_1 _750_ (.A1_N(net42),
    .A2_N(_277_),
    .B1(_278_),
    .B2(net41),
    .Y(_279_));
 sky130_fd_sc_hd__nand4_1 _751_ (.A(_384_),
    .B(_050_),
    .C(_276_),
    .D(_279_),
    .Y(_280_));
 sky130_fd_sc_hd__nand2_1 _752_ (.A(_384_),
    .B(_268_),
    .Y(_281_));
 sky130_fd_sc_hd__nand3_1 _753_ (.A(stage1_valid),
    .B(_280_),
    .C(_281_),
    .Y(_282_));
 sky130_fd_sc_hd__o21ai_0 _754_ (.A1(_266_),
    .A2(_122_),
    .B1(net40),
    .Y(_283_));
 sky130_fd_sc_hd__o21ai_0 _755_ (.A1(_106_),
    .A2(_167_),
    .B1(_283_),
    .Y(_284_));
 sky130_fd_sc_hd__o21ai_0 _756_ (.A1(net37),
    .A2(_273_),
    .B1(_137_),
    .Y(_285_));
 sky130_fd_sc_hd__a21oi_1 _757_ (.A1(_216_),
    .A2(_285_),
    .B1(net42),
    .Y(_286_));
 sky130_fd_sc_hd__o21ai_0 _758_ (.A1(_421_),
    .A2(_430_),
    .B1(_185_),
    .Y(_287_));
 sky130_fd_sc_hd__nand2_1 _759_ (.A(_050_),
    .B(_287_),
    .Y(_288_));
 sky130_fd_sc_hd__a211oi_1 _760_ (.A1(net42),
    .A2(_284_),
    .B1(_286_),
    .C1(_288_),
    .Y(_289_));
 sky130_fd_sc_hd__nand2_1 _761_ (.A(\stage1_x[0] ),
    .B(net40),
    .Y(_290_));
 sky130_fd_sc_hd__o32ai_1 _762_ (.A1(\stage1_x[0] ),
    .A2(_038_),
    .A3(_254_),
    .B1(_290_),
    .B2(_217_),
    .Y(_291_));
 sky130_fd_sc_hd__nor2b_1 _763_ (.A(net34),
    .B_N(stage1_valid),
    .Y(_292_));
 sky130_fd_sc_hd__o21ai_0 _764_ (.A1(_050_),
    .A2(_291_),
    .B1(_292_),
    .Y(_293_));
 sky130_fd_sc_hd__nor2_1 _765_ (.A(stage1_valid),
    .B(net17),
    .Y(_294_));
 sky130_fd_sc_hd__nor2_1 _766_ (.A(net43),
    .B(_294_),
    .Y(_295_));
 sky130_fd_sc_hd__o21a_1 _767_ (.A1(_289_),
    .A2(_293_),
    .B1(_295_),
    .X(_296_));
 sky130_fd_sc_hd__o21ai_0 _768_ (.A1(_221_),
    .A2(_238_),
    .B1(\stage1_x[0] ),
    .Y(_297_));
 sky130_fd_sc_hd__a21oi_1 _769_ (.A1(net40),
    .A2(_174_),
    .B1(\stage1_x[1] ),
    .Y(_298_));
 sky130_fd_sc_hd__a311oi_1 _770_ (.A1(\stage1_x[1] ),
    .A2(_125_),
    .A3(_297_),
    .B1(_298_),
    .C1(_421_),
    .Y(_299_));
 sky130_fd_sc_hd__nand2_1 _771_ (.A(_061_),
    .B(_266_),
    .Y(_300_));
 sky130_fd_sc_hd__a21oi_1 _772_ (.A1(net41),
    .A2(_094_),
    .B1(_082_),
    .Y(_301_));
 sky130_fd_sc_hd__a31oi_1 _773_ (.A1(net40),
    .A2(_080_),
    .A3(_232_),
    .B1(_301_),
    .Y(_302_));
 sky130_fd_sc_hd__a31oi_1 _774_ (.A1(_189_),
    .A2(_300_),
    .A3(_302_),
    .B1(net42),
    .Y(_303_));
 sky130_fd_sc_hd__nor3_1 _775_ (.A(net36),
    .B(_067_),
    .C(_209_),
    .Y(_304_));
 sky130_fd_sc_hd__a21oi_1 _776_ (.A1(net42),
    .A2(_421_),
    .B1(_232_),
    .Y(_305_));
 sky130_fd_sc_hd__o21ai_0 _777_ (.A1(_125_),
    .A2(_305_),
    .B1(net34),
    .Y(_306_));
 sky130_fd_sc_hd__o41ai_1 _778_ (.A1(_299_),
    .A2(_303_),
    .A3(_304_),
    .A4(_306_),
    .B1(_295_),
    .Y(_307_));
 sky130_fd_sc_hd__nand2_1 _779_ (.A(\stage1_x[0] ),
    .B(net37),
    .Y(_308_));
 sky130_fd_sc_hd__a21oi_1 _780_ (.A1(_088_),
    .A2(_308_),
    .B1(_048_),
    .Y(_309_));
 sky130_fd_sc_hd__a2111oi_0 _781_ (.A1(net37),
    .A2(_205_),
    .B1(_309_),
    .C1(net35),
    .D1(_384_),
    .Y(_310_));
 sky130_fd_sc_hd__o22ai_1 _782_ (.A1(_125_),
    .A2(_167_),
    .B1(_247_),
    .B2(net37),
    .Y(_311_));
 sky130_fd_sc_hd__o211ai_1 _783_ (.A1(net37),
    .A2(_203_),
    .B1(_255_),
    .C1(\stage1_x[0] ),
    .Y(_312_));
 sky130_fd_sc_hd__o21ai_0 _784_ (.A1(\stage1_x[0] ),
    .A2(_311_),
    .B1(_312_),
    .Y(_313_));
 sky130_fd_sc_hd__a21oi_1 _785_ (.A1(\stage1_x[0] ),
    .A2(_038_),
    .B1(_392_),
    .Y(_314_));
 sky130_fd_sc_hd__o21ai_0 _786_ (.A1(net41),
    .A2(net37),
    .B1(net40),
    .Y(_315_));
 sky130_fd_sc_hd__a22oi_1 _787_ (.A1(_096_),
    .A2(_232_),
    .B1(_198_),
    .B2(_315_),
    .Y(_316_));
 sky130_fd_sc_hd__o21ai_1 _788_ (.A1(_396_),
    .A2(_314_),
    .B1(_316_),
    .Y(_317_));
 sky130_fd_sc_hd__nand2_1 _789_ (.A(\stage1_x[0] ),
    .B(_195_),
    .Y(_318_));
 sky130_fd_sc_hd__a211oi_1 _790_ (.A1(_203_),
    .A2(_318_),
    .B1(net38),
    .C1(_050_),
    .Y(_319_));
 sky130_fd_sc_hd__a211o_1 _791_ (.A1(net35),
    .A2(_317_),
    .B1(_319_),
    .C1(net34),
    .X(_320_));
 sky130_fd_sc_hd__a22oi_1 _792_ (.A1(_310_),
    .A2(_313_),
    .B1(_320_),
    .B2(\stage1_x[7] ),
    .Y(_321_));
 sky130_fd_sc_hd__o2bb2ai_1 _793_ (.A1_N(_282_),
    .A2_N(_296_),
    .B1(_307_),
    .B2(_321_),
    .Y(_007_));
 sky130_fd_sc_hd__o21ai_0 _794_ (.A1(net42),
    .A2(_396_),
    .B1(_121_),
    .Y(_322_));
 sky130_fd_sc_hd__o21ai_0 _795_ (.A1(net41),
    .A2(_418_),
    .B1(_040_),
    .Y(_323_));
 sky130_fd_sc_hd__o21ai_0 _796_ (.A1(net42),
    .A2(_137_),
    .B1(net37),
    .Y(_324_));
 sky130_fd_sc_hd__nor3_1 _797_ (.A(_069_),
    .B(_266_),
    .C(_217_),
    .Y(_325_));
 sky130_fd_sc_hd__o2bb2ai_1 _798_ (.A1_N(_069_),
    .A2_N(_323_),
    .B1(_324_),
    .B2(_325_),
    .Y(_326_));
 sky130_fd_sc_hd__a22o_1 _799_ (.A1(_392_),
    .A2(_322_),
    .B1(_326_),
    .B2(net40),
    .X(_327_));
 sky130_fd_sc_hd__xnor2_1 _800_ (.A(\stage1_x[0] ),
    .B(_248_),
    .Y(_328_));
 sky130_fd_sc_hd__a21oi_1 _801_ (.A1(\stage1_x[1] ),
    .A2(_262_),
    .B1(_328_),
    .Y(_329_));
 sky130_fd_sc_hd__o21ai_0 _802_ (.A1(net40),
    .A2(_137_),
    .B1(net35),
    .Y(_330_));
 sky130_fd_sc_hd__nand3_1 _803_ (.A(\stage1_x[0] ),
    .B(_025_),
    .C(_330_),
    .Y(_331_));
 sky130_fd_sc_hd__o211ai_1 _804_ (.A1(_094_),
    .A2(_329_),
    .B1(_331_),
    .C1(_292_),
    .Y(_332_));
 sky130_fd_sc_hd__a21oi_1 _805_ (.A1(net35),
    .A2(_327_),
    .B1(_332_),
    .Y(_333_));
 sky130_fd_sc_hd__a21oi_1 _806_ (.A1(\stage1_x[1] ),
    .A2(_082_),
    .B1(_248_),
    .Y(_334_));
 sky130_fd_sc_hd__o211ai_1 _807_ (.A1(_033_),
    .A2(_038_),
    .B1(\stage1_x[0] ),
    .C1(_048_),
    .Y(_335_));
 sky130_fd_sc_hd__o31a_1 _808_ (.A1(\stage1_x[0] ),
    .A2(net35),
    .A3(_334_),
    .B1(_335_),
    .X(_336_));
 sky130_fd_sc_hd__a21oi_1 _809_ (.A1(\stage1_x[0] ),
    .A2(_217_),
    .B1(_429_),
    .Y(_337_));
 sky130_fd_sc_hd__or3_1 _810_ (.A(_025_),
    .B(_421_),
    .C(_337_),
    .X(_338_));
 sky130_fd_sc_hd__o21ai_0 _811_ (.A1(net37),
    .A2(_336_),
    .B1(_338_),
    .Y(_339_));
 sky130_fd_sc_hd__or2_2 _812_ (.A(_168_),
    .B(_273_),
    .X(_340_));
 sky130_fd_sc_hd__nand2b_1 _813_ (.A_N(net42),
    .B(net41),
    .Y(_341_));
 sky130_fd_sc_hd__o22ai_1 _814_ (.A1(_067_),
    .A2(_341_),
    .B1(_209_),
    .B2(_094_),
    .Y(_342_));
 sky130_fd_sc_hd__a21oi_1 _815_ (.A1(_429_),
    .A2(_340_),
    .B1(_342_),
    .Y(_343_));
 sky130_fd_sc_hd__nor2_1 _816_ (.A(_429_),
    .B(_248_),
    .Y(_344_));
 sky130_fd_sc_hd__o211a_1 _817_ (.A1(_404_),
    .A2(_195_),
    .B1(stage1_valid),
    .C1(net34),
    .X(_345_));
 sky130_fd_sc_hd__o221ai_1 _818_ (.A1(net38),
    .A2(_343_),
    .B1(_344_),
    .B2(_157_),
    .C1(_345_),
    .Y(_346_));
 sky130_fd_sc_hd__nand2b_1 _819_ (.A_N(stage1_valid),
    .B(net16),
    .Y(_347_));
 sky130_fd_sc_hd__a21oi_1 _820_ (.A1(_100_),
    .A2(_347_),
    .B1(net43),
    .Y(_348_));
 sky130_fd_sc_hd__o21ai_0 _821_ (.A1(_339_),
    .A2(_346_),
    .B1(_348_),
    .Y(_349_));
 sky130_fd_sc_hd__nor2b_1 _822_ (.A(net36),
    .B_N(\stage1_x[1] ),
    .Y(_350_));
 sky130_fd_sc_hd__xnor2_1 _823_ (.A(_074_),
    .B(_350_),
    .Y(_351_));
 sky130_fd_sc_hd__o221ai_1 _824_ (.A1(net41),
    .A2(_080_),
    .B1(_082_),
    .B2(net36),
    .C1(\stage1_x[0] ),
    .Y(_352_));
 sky130_fd_sc_hd__o21ai_0 _825_ (.A1(\stage1_x[0] ),
    .A2(_351_),
    .B1(_352_),
    .Y(_353_));
 sky130_fd_sc_hd__nand2_1 _826_ (.A(\stage1_x[0] ),
    .B(_220_),
    .Y(_354_));
 sky130_fd_sc_hd__xnor2_1 _827_ (.A(_047_),
    .B(_354_),
    .Y(_355_));
 sky130_fd_sc_hd__o221ai_1 _828_ (.A1(net37),
    .A2(_353_),
    .B1(_355_),
    .B2(_094_),
    .C1(net34),
    .Y(_356_));
 sky130_fd_sc_hd__o221ai_1 _829_ (.A1(_392_),
    .A2(_396_),
    .B1(_125_),
    .B2(net41),
    .C1(\stage1_x[0] ),
    .Y(_357_));
 sky130_fd_sc_hd__o311a_1 _830_ (.A1(\stage1_x[0] ),
    .A2(_068_),
    .A3(_262_),
    .B1(_357_),
    .C1(net35),
    .X(_358_));
 sky130_fd_sc_hd__o221ai_1 _831_ (.A1(stage1_valid),
    .A2(net16),
    .B1(_356_),
    .B2(_358_),
    .C1(_270_),
    .Y(_359_));
 sky130_fd_sc_hd__nand2_1 _832_ (.A(\stage1_x[0] ),
    .B(_040_),
    .Y(_360_));
 sky130_fd_sc_hd__nor3_1 _833_ (.A(\stage1_x[1] ),
    .B(_418_),
    .C(_262_),
    .Y(_361_));
 sky130_fd_sc_hd__a31oi_1 _834_ (.A1(\stage1_x[1] ),
    .A2(_125_),
    .A3(_071_),
    .B1(_361_),
    .Y(_362_));
 sky130_fd_sc_hd__o21ai_1 _835_ (.A1(net41),
    .A2(_430_),
    .B1(net37),
    .Y(_363_));
 sky130_fd_sc_hd__o21ai_0 _836_ (.A1(\stage1_x[1] ),
    .A2(_164_),
    .B1(_363_),
    .Y(_364_));
 sky130_fd_sc_hd__o22ai_1 _837_ (.A1(_360_),
    .A2(_362_),
    .B1(_364_),
    .B2(\stage1_x[0] ),
    .Y(_365_));
 sky130_fd_sc_hd__o21ai_0 _838_ (.A1(net42),
    .A2(_106_),
    .B1(_125_),
    .Y(_366_));
 sky130_fd_sc_hd__a221oi_1 _839_ (.A1(net42),
    .A2(_266_),
    .B1(_366_),
    .B2(net41),
    .C1(_187_),
    .Y(_367_));
 sky130_fd_sc_hd__nor3_1 _840_ (.A(net42),
    .B(net38),
    .C(_203_),
    .Y(_368_));
 sky130_fd_sc_hd__nor3b_1 _841_ (.A(_368_),
    .B(_094_),
    .C_N(_209_),
    .Y(_369_));
 sky130_fd_sc_hd__a2111oi_2 _842_ (.A1(net36),
    .A2(_365_),
    .B1(_367_),
    .C1(_369_),
    .D1(net34),
    .Y(_370_));
 sky130_fd_sc_hd__o22ai_1 _843_ (.A1(_333_),
    .A2(_349_),
    .B1(_359_),
    .B2(_370_),
    .Y(_008_));
 sky130_fd_sc_hd__mux2i_1 _845_ (.A0(\stage1_x[6] ),
    .A1(net14),
    .S(net6),
    .Y(_372_));
 sky130_fd_sc_hd__nor2_1 _846_ (.A(net43),
    .B(_372_),
    .Y(_009_));
 sky130_fd_sc_hd__mux2i_1 _847_ (.A0(net35),
    .A1(net13),
    .S(net6),
    .Y(_373_));
 sky130_fd_sc_hd__nor2_1 _848_ (.A(net43),
    .B(_373_),
    .Y(_010_));
 sky130_fd_sc_hd__mux2i_1 _849_ (.A0(net37),
    .A1(net12),
    .S(net6),
    .Y(_374_));
 sky130_fd_sc_hd__nor2_1 _850_ (.A(net43),
    .B(_374_),
    .Y(_011_));
 sky130_fd_sc_hd__mux2i_1 _851_ (.A0(\stage1_x[3] ),
    .A1(net11),
    .S(net6),
    .Y(_375_));
 sky130_fd_sc_hd__nor2_1 _852_ (.A(net43),
    .B(_375_),
    .Y(_012_));
 sky130_fd_sc_hd__mux2i_1 _853_ (.A0(\stage1_x[2] ),
    .A1(net10),
    .S(net6),
    .Y(_376_));
 sky130_fd_sc_hd__nor2_1 _854_ (.A(net43),
    .B(_376_),
    .Y(_013_));
 sky130_fd_sc_hd__mux2i_1 _855_ (.A0(\stage1_x[1] ),
    .A1(net9),
    .S(net6),
    .Y(_377_));
 sky130_fd_sc_hd__nor2_1 _856_ (.A(net43),
    .B(_377_),
    .Y(_014_));
 sky130_fd_sc_hd__mux2i_1 _857_ (.A0(\stage1_x[0] ),
    .A1(net8),
    .S(net6),
    .Y(_378_));
 sky130_fd_sc_hd__nor2_1 _858_ (.A(net43),
    .B(_378_),
    .Y(_015_));
 sky130_fd_sc_hd__o21bai_1 _859_ (.A1(net34),
    .A2(_426_),
    .B1_N(_085_),
    .Y(_379_));
 sky130_fd_sc_hd__nand2b_1 _860_ (.A_N(stage1_valid),
    .B(net25),
    .Y(_380_));
 sky130_fd_sc_hd__a21oi_1 _861_ (.A1(_379_),
    .A2(_380_),
    .B1(net43),
    .Y(_016_));
 sky130_fd_sc_hd__mux2i_1 _862_ (.A0(\stage1_x[7] ),
    .A1(net15),
    .S(net6),
    .Y(_381_));
 sky130_fd_sc_hd__nor2_1 _863_ (.A(net43),
    .B(_381_),
    .Y(_017_));
 sky130_fd_sc_hd__nor2b_1 _864_ (.A(net43),
    .B_N(net6),
    .Y(_018_));
 sky130_fd_sc_hd__conb_1 _866__1 (.LO(exp_out[10]));
 sky130_fd_sc_hd__conb_1 _867__2 (.LO(exp_out[11]));
 sky130_fd_sc_hd__conb_1 _868__3 (.LO(exp_out[12]));
 sky130_fd_sc_hd__conb_1 _869__4 (.LO(exp_out[13]));
 sky130_fd_sc_hd__conb_1 _870__5 (.LO(exp_out[14]));
 sky130_fd_sc_hd__conb_1 _871__6 (.LO(exp_out[15]));
 sky130_fd_sc_hd__clkbuf_8 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__clkbuf_8 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__clkbuf_8 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkinvlp_4 clkload0 (.A(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[0]$_SDFFE_PP0P_  (.D(_008_),
    .Q(net16),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[1]$_SDFFE_PP0P_  (.D(_007_),
    .Q(net17),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[2]$_SDFFE_PP0P_  (.D(_006_),
    .Q(net18),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[3]$_SDFFE_PP0P_  (.D(_005_),
    .Q(net19),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[4]$_SDFFE_PP0P_  (.D(_004_),
    .Q(net20),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[5]$_SDFFE_PP0P_  (.D(_003_),
    .Q(net21),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[6]$_SDFFE_PP0P_  (.D(_002_),
    .Q(net22),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[7]$_SDFFE_PP0P_  (.D(_001_),
    .Q(net23),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[8]$_SDFFE_PP0P_  (.D(_000_),
    .Q(net24),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \exp_out[9]$_SDFFE_PP0P_  (.D(_016_),
    .Q(net25),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input10 (.A(x_in[1]),
    .X(net9));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input11 (.A(x_in[2]),
    .X(net10));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input12 (.A(x_in[3]),
    .X(net11));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input13 (.A(x_in[4]),
    .X(net12));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input14 (.A(x_in[5]),
    .X(net13));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input15 (.A(x_in[6]),
    .X(net14));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input16 (.A(x_in[7]),
    .X(net15));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input7 (.A(enable),
    .X(net6));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input8 (.A(rst),
    .X(net7));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input9 (.A(x_in[0]),
    .X(net8));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output17 (.A(net16),
    .X(exp_out[0]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output18 (.A(net17),
    .X(exp_out[1]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output19 (.A(net18),
    .X(exp_out[2]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output20 (.A(net19),
    .X(exp_out[3]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output21 (.A(net20),
    .X(exp_out[4]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output22 (.A(net21),
    .X(exp_out[5]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output23 (.A(net22),
    .X(exp_out[6]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output24 (.A(net23),
    .X(exp_out[7]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output25 (.A(net24),
    .X(exp_out[8]));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output26 (.A(net25),
    .X(exp_out[9]));
 sky130_fd_sc_hd__buf_4 place35 (.A(\stage1_x[6] ),
    .X(net34));
 sky130_fd_sc_hd__buf_4 place36 (.A(\stage1_x[5] ),
    .X(net35));
 sky130_fd_sc_hd__buf_4 place37 (.A(\stage1_x[5] ),
    .X(net36));
 sky130_fd_sc_hd__buf_4 place38 (.A(\stage1_x[4] ),
    .X(net37));
 sky130_fd_sc_hd__buf_4 place39 (.A(\stage1_x[3] ),
    .X(net38));
 sky130_fd_sc_hd__buf_4 place40 (.A(\stage1_x[3] ),
    .X(net39));
 sky130_fd_sc_hd__buf_4 place41 (.A(\stage1_x[2] ),
    .X(net40));
 sky130_fd_sc_hd__buf_4 place42 (.A(\stage1_x[1] ),
    .X(net41));
 sky130_fd_sc_hd__buf_4 place43 (.A(\stage1_x[0] ),
    .X(net42));
 sky130_fd_sc_hd__buf_4 place44 (.A(net7),
    .X(net43));
 sky130_fd_sc_hd__dfxtp_1 \stage1_valid$_SDFF_PP0_  (.D(_018_),
    .Q(stage1_valid),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_2 \stage1_x[0]$_SDFFE_PP0P_  (.D(_015_),
    .Q(\stage1_x[0] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_2 \stage1_x[1]$_SDFFE_PP0P_  (.D(_014_),
    .Q(\stage1_x[1] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[2]$_SDFFE_PP0P_  (.D(_013_),
    .Q(\stage1_x[2] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[3]$_SDFFE_PP0P_  (.D(_012_),
    .Q(\stage1_x[3] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[4]$_SDFFE_PP0P_  (.D(_011_),
    .Q(\stage1_x[4] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[5]$_SDFFE_PP0P_  (.D(_010_),
    .Q(\stage1_x[5] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[6]$_SDFFE_PP0P_  (.D(_009_),
    .Q(\stage1_x[6] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \stage1_x[7]$_SDFFE_PP0P_  (.D(_017_),
    .Q(\stage1_x[7] ),
    .CLK(clknet_1_0__leaf_clk));
endmodule
