from pyspark.sql import SparkSession
import sys
from pyspark.sql.functions import format_string, date_format, col, create_map, lit
from itertools import chain
spark = SparkSession.builder.appName("project").config("spark.some.config.option","some-value").getOrCreate()
graduation = spark.read.format('csv').options(header='true',inferschema='true', delimiter='\t').load('/user/hm74/NYCOpenData/kybe-9iex.tsv.gz')
graduation.createOrReplaceTempView("graduation")
schoolToZip = {
    '02M570':'10001',
    '01M292':'10002','01M448':'10002','01M458':'10002','01M509':'10002','01M515':'10002','01M539':'10002','01M650':'10002','01M696':'10002','02M294':'10002','02M298':'10002','02M305':'10002','02M308':'10002','02M394':'10002','02M445':'10002','02M543':'10002','02M545':'10002',
    '02M374':'10003','02M399':'10003','02M407':'10003','02M420':'10003','02M438':'10003','02M460':'10003','02M533':'10003','02M546':'10003','02M575':'10003','02M586':'10003',
    '02M316':'10004','02M418':'10004','02M580':'10004',
    '02M425':'10006','02M489':'10006',
    '01M450':'10009',
    '02M047':'10010','02M411':'10010','02M413':'10010','02M439':'10010',
    '02M313':'10011','02M392':'10011','02M412':'10011','02M414':'10011','02M419':'10011','02M422':'10011','02M429':'10011','02M437':'10011','02M440':'10011','02M534':'10011','02M550':'10011','02M600':'10011','02M605':'10011','02M690':'10011',
    '02M376':'10013','02M615':'10013',
    '02M560':'10014',
    '02M427':'10016','02M432':'10016','02M500':'10016','02M620':'10016',
    '02M139':'10019','02M288':'10019','02M296':'10019','02M300':'10019','02M303':'10019','02M393':'10019','02M400':'10019','02M507':'10019','02M535':'10019','02M542':'10019','02M544':'10019','02M625':'10019',
    '02M416':'10021',
    '02M630':'10022',
    '03M283':'10023','03M299':'10023','03M307':'10023','03M485':'10023','03M492':'10023','03M494':'10023','03M541':'10023','03M859':'10023',
    '03M402':'10024','03M403':'10024','03M404':'10024','03M417':'10024','03M470':'10024',
    '03M505':'10025',
    '03M415':'10026','03M860':'10026',
    '05M362':'10027','05M369':'10027',
    '04M372':'10029','04M435':'10029','04M495':'10029','04M555':'10029','04M610':'10029','04M635':'10029','04M680':'10029',
    '05M304':'10030','05M670':'10030','05M685':'10030',
    '05M692':'10031','06M540':'10031',
    '06M346':'10032','06M552':'10032',
    '06M348':'10033',
    '06M423':'10034',
    '04M409':'10035','04M695':'10035','05M157':'10035','05M285':'10035','05M469':'10035',
    '02M408':'10036','02M529':'10036','02M531':'10036','03M479':'10036',
    '02M135':'10038','02M280':'10038','02M282':'10038','02M520':'10038',
    '05M499':'10039',
    '06M293':'10040','06M462':'10040','06M463':'10040','06M467':'10040','06M468':'10040',
    '02M449':'10065','02M459':'10065','02M519':'10065','02M565':'10065',
    '02M655':'10128','05M367':'10128',
    '02M475':'10282',
    '31R080':'10301','31R450':'10301','31R600':'10301',
    '31R445':'10302',
    '31R470':'10304',
    '31R440':'10306','31R605':'10306',
    '31R455':'10312',
    '31R047':'10314','31R064':'10314','31R460':'10314',
    '07X381':'10451','07X427':'10451','07X470':'10451','07X522':'10451','07X527':'10451','07X547':'10451','07X548':'10451','07X551':'10451','07X600':'10451','07X670':'10451','09X505':'10451',
    '09X327':'10452',
    '09X365':'10453',
    '07X221':'10454','07X223':'10454','07X334':'10454',
    '07X259':'10455','07X473':'10455','07X495':'10455','07X500':'10455','07X520':'10455','07X557':'10455','07X655':'10455',
    '07X379':'10456','08X559':'10456','08X650':'10456','09X250':'10456','09X260':'10456','09X297':'10456','09X324':'10456','09X403':'10456','09X404':'10456','09X517':'10456','09X543':'10456','12X245':'10456','12X267':'10456','12X479':'10456',
    '09X227':'10457','09X231':'10457','09X239':'10457','09X241':'10457','09X252':'10457','09X263':'10457','09X276':'10457','09X329':'10457','09X350':'10457','09X412':'10457','09X413':'10457','09X414':'10457','09X525':'10457','09X564':'10457','10X225':'10457','10X319':'10457','10X410':'10457',
    '10X243':'10458','10X264':'10458','10X374':'10458','10X434':'10458','10X435':'10458','10X437':'10458','10X438':'10458','10X439':'10458','10X524':'10458','10X565':'10458','10X660':'10458',
    '08X269':'10459','08X332':'10459','08X530':'10459','08X686':'10459','12X248':'10459','12X278':'10459','12X321':'10459','12X446':'10459','12X480':'10459',
    '12X251':'10460','12X262':'10460','12X271':'10460','12X372':'10460','12X511':'10460','12X682':'10460','12X684':'10460',
    '08X293':'10461','08X320':'10461','08X348':'10461','08X349':'10461','08X405':'10461','08X558':'10461',
    '11X418':'10462',
    '10X141':'10463','10X213':'10463','10X237':'10463','10X284':'10463','10X368':'10463','10X397':'10463','10X475':'10463','10X477':'10463','10X546':'10463',
    '11X270':'10466','11X513':'10466','11X514':'10466',
    '11X253':'10467','11X265':'10467','11X275':'10467','11X290':'10467','11X425':'10467','11X544':'10467','11X545':'10467',
    '10X268':'10468','10X342':'10468','10X351':'10468','10X353':'10468','10X430':'10468','10X433':'10468','10X440':'10468','10X442':'10468','10X445':'10468','10X549':'10468','10X696':'10468',
    '11X288':'10469','11X299':'10469','11X415':'10469','11X508':'10469','11X509':'10469','11X541':'10469','11X542':'10469',
    '12X242':'10472','12X388':'10472','12X478':'10472','12X521':'10472','12X550':'10472','12X680':'10472','12X690':'10472','12X692':'10472',
    '08X282':'10473','08X295':'10473','08X305':'10473','08X312':'10473','08X367':'10473','08X376':'10473','08X377':'10473','08X432':'10473','08X450':'10473','08X452':'10473','08X519':'10473','08X537':'10473','08X540':'10473','08X560':'10473','08X561':'10473',
    '11X249':'10475','11X455':'10475',
    '03M490':'10701',
    '24Q264':'11101','24Q267':'11101','24Q299':'11101','24Q520':'11101','24Q530':'11101','24Q560':'11101','24Q600':'11101','24Q610':'11101','30Q301':'11101','30Q502':'11101','30Q555':'11101','30Q575':'11101',
    '30Q286':'11102',
    '30Q445':'11103',
    '30Q258':'11106','30Q450':'11106','30Q501':'11106','30Q580':'11106',
    '13K350':'11201','13K419':'11201','13K439':'11201','13K483':'11201','13K509':'11201','13K527':'11201','13K605':'11201','13K674':'11201','15K423':'11201','15K429':'11201','15K497':'11201','15K519':'11201','15K520':'11201',
    '17K470':'11203','17K531':'11203','17K533':'11203','17K544':'11203','17K546':'11203','17K745':'11203','18K415':'11203','18K563':'11203','18K569':'11203','18K589':'11203','18K629':'11203',
    '20K505':'11204','20K609':'11204',
    '13K265':'11205','13K412':'11205','13K616':'11205','13K670':'11205',
    '14K071':'11206','14K322':'11206','14K449':'11206','14K454':'11206','14K586':'11206','14K614':'11206',
    '19K409':'11207','19K435':'11207','19K502':'11207','19K504':'11207','19K507':'11207','19K510':'11207','19K660':'11207',
    '19K420':'11208','19K583':'11208','19K615':'11208','19K618':'11208','19K639':'11208','19K659':'11208','19K683':'11208','19K764':'11208',
    '20K490':'11209',
    '22K405':'11210',
    '14K474':'11211','14K477':'11211','14K478':'11211','14K488':'11211','14K558':'11211','14K561':'11211','14K640':'11211','14K685':'11211','17K479':'11211',
    '17K568':'11212','18K673':'11212','23K514':'11212','23K643':'11212','23K647':'11212','23K697':'11212',
    '16K455':'11213','16K669':'11213','16K765':'11213','17K122':'11213','17K625':'11213','17K751':'11213',
    '20K445':'11214','21K337':'11214','21K348':'11214','21K400':'11214','21K468':'11214','21K559':'11214','21K572':'11214','21K690':'11214',
    '15K462':'11215','15K463':'11215','15K464':'11215','15K684':'11215',
    '13K336':'11216','13K553':'11216','13K575':'11216','13K595':'11216',
    '13K430':'11217','15K530':'11217','15K592':'11217','15K656':'11217',
    '22K555':'11218',
    '15K529':'11219',
    '20K485':'11220',
    '16K393':'11221','16K498':'11221','16K688':'11221','32K545':'11221','32K552':'11221','32K556':'11221','32K564':'11221',
    '14K610':'11222','14K632':'11222',
    '21K540':'11223',
    '21K344':'11224','21K728':'11224',
    '17K440':'11225','17K489':'11225','17K524':'11225','17K528':'11225','17K547':'11225','17K548':'11225','17K590':'11225','17K600':'11225','17K646':'11225',
    '17K382':'11226','17K408':'11226','17K459':'11226','17K469':'11226','17K537':'11226','17K539':'11226','17K543':'11226',
    '22K425':'11229',
    '21K525':'11230',
    '02M551':'11231','15K027':'11231','15K448':'11231','15K698':'11231',
    '15K667':'11232',
    '23K493':'11233','23K644':'11233','23K645':'11233',
    '21K410':'11235','21K620':'11235','22K495':'11235','22K535':'11235','22K611':'11235','22K630':'11235',
    '18K515':'11236','18K566':'11236','18K567':'11236','18K576':'11236','18K578':'11236','18K617':'11236','18K633':'11236','18K635':'11236','18K637':'11236','18K642':'11236','22K585':'11236',
    '32K168':'11237','32K403':'11237','32K480':'11237','32K549':'11237','32K554':'11237',
    '13K499':'11238','13K594':'11238','18K500':'11238',
    '19K404':'11239',
    '25Q240':'11354','25Q241':'11354','25Q460':'11354','25Q540':'11354',
    '25Q263':'11355','25Q281':'11355',
    '25Q285':'11358',
    '26Q495':'11361',
    '26Q415':'11364',
    '26Q430':'11365',
    '25Q252':'11366','25Q670':'11366',
    '25Q425':'11367','25Q525':'11367','25Q792':'11367',
    '24Q550':'11368',
    '24Q236':'11373','24Q293':'11373','24Q296':'11373','24Q455':'11373','24Q585':'11373','24Q744':'11373',
    '28Q167':'11375','28Q440':'11375','28Q686':'11375',
    '24Q485':'11385',
    '29Q243':'11411','29Q313':'11411','29Q492':'11411','29Q494':'11411','29Q496':'11411','29Q498':'11411',
    '29Q259':'11412',
    '29Q248':'11413','29Q265':'11413','29Q272':'11413','29Q283':'11413','29Q420':'11413',
    '27Q650':'11416',
    '27Q308':'11417','27Q480':'11417',
    '27Q475':'11418',
    '27Q314':'11420',
    '29Q326':'11423',
    '26Q566':'11426',
    '26Q435':'11427',
    '28Q310':'11432','28Q325':'11432','28Q328':'11432','28Q338':'11432','28Q350':'11432','28Q470':'11432','28Q505':'11432','28Q620':'11432','28Q680':'11432','28Q896':'11432',
    '28Q284':'11433',
    '27Q261':'11434','28Q690':'11434','29Q327':'11434',
    '28Q687':'11451',
    '27Q260':'11691','27Q302':'11691','27Q309':'11691','27Q465':'11691',
    '27Q262':'11694','27Q323':'11694','27Q324':'11694','27Q410':'11694',
}
mapping_expr = create_map([lit(x) for x in chain(*schoolToZip.items())])
graduation_with_zip = graduation.withColumn("Zip", mapping_expr.getItem(col("DBN")))
graduation_with_zip.createOrReplaceTempView("graduation_with_zip")
#graduation_with_zip.show(1)
#check = spark.sql("select DBN from graduation_with_zip where Zip=null")
#check.show()
avg_grad_rate_across_program_and_cohort_yr = spark.sql("select Zip,DBN,`Demographic Variable`, avg(`Total Grads % of cohort`) as graduation_rate from graduation_with_zip where `Demographic Category`='Ethnicity' and `Total Grads % of cohort`<>'s' group by Zip,DBN,`Demographic Variable`")
avg_grad_rate_across_program_and_cohort_yr.createOrReplaceTempView("avg_grad_rate_across_program_and_cohort_yr")
avg_grad_rate_across_zip = spark.sql("select Zip,`Demographic Variable`, avg(graduation_rate) as graduation_rate from avg_grad_rate_across_program_and_cohort_yr group by Zip,`Demographic Variable`")
avg_grad_rate_across_zip.createOrReplaceTempView("avg_grad_rate_across_zip")
school_result = spark.sql("select t1.Zip as Zip, t1.DBN as DBN, t1.`Demographic Variable` as r1, t2.`Demographic Variable` as r2, abs(t1.graduation_rate-t2.graduation_rate) as disparity, t1.graduation_rate, t2.graduation_rate from avg_grad_rate_across_program_and_cohort_yr t1, avg_grad_rate_across_program_and_cohort_yr t2 where t1.DBN=t2.DBN and t1.`Demographic Variable`<t2.`Demographic Variable` order by disparity desc")
school_result.show(20)
zip_result = spark.sql("select t1.Zip as Zip, t1.`Demographic Variable` as r1, t2.`Demographic Variable` as r2, abs(t1.graduation_rate-t2.graduation_rate) as disparity, t1.graduation_rate, t2.graduation_rate from avg_grad_rate_across_zip t1, avg_grad_rate_across_zip t2 where t1.Zip=t2.Zip and t1.`Demographic Variable`<t2.`Demographic Variable` order by disparity desc")
zip_result.show(15)

check_white=spark.sql("select * from avg_grad_rate_across_program_and_cohort_yr where Zip='10457' and `Demographic Variable`='White'")
check_white.show()
check_native=spark.sql("select * from avg_grad_rate_across_program_and_cohort_yr where Zip='10457' and `Demographic Variable`='Native American'")
check_native.show()

check_white_2=spark.sql("select * from avg_grad_rate_across_program_and_cohort_yr where Zip='10459' and `Demographic Variable`='White'")
check_white_2.show() 

#check_white_3=spark.sql("select * from avg_grad_rate_across_program_and_cohort_yr where Zip='10455' and `Demographic Variable`='White'")
#check_white_3.show()