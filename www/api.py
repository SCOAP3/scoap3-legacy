from invenio.dbquery import run_sql
from invenio.webpage import pagefooteronly, pageheaderonly
from invenio.urlutils import redirect_to_url
from invenio.mailutils import send_email
from invenio.access_control_admin import acc_is_user_in_role, acc_get_role_id
from invenio.webuser import collect_user_info
from invenio.web_api_key import create_new_web_api_key
import json


def index(req):
  return ""


def init_db():
    _prepare_country_db()
    _prepare_institut_db()

    def_country = ("Austria",
                   "Belgium",
                   "Canada",
                   "China",
                   "Czech Republic",
                   "Denmark",
                   "Finland",
                   "France",
                   "Germany",
                   "Greece",
                   "Hong-Kong",
                   "Hungary",
                   "Italy",
                   "Japan",
                   "Armenia",
                   "Azerbaijan",
                   "Belarus",
                   "Cuba",
                   "North Korea",
                   "Georgia",
                   "Kazakhstan",
                   "Moldova",
                   "Mongolia",
                   "Ukraine",
                   "Uzbekistan",
                   "Vietnam",
                   "South Korea",
                   "Mexico",
                   "Netherlands",
                   "Norway",
                   "Poland",
                   "Portugal",
                   "Slovak Republik",
                   "South Africa",
                   "Spain",
                   "Sweden",
                   "Switzerland",
                   "Turkey",
                   "United Kingdom",
                   "United States")

    for country in def_country:
        run_sql("INSERT INTO country (name) VALUES('%s')" % (country,))

    def_institutes = (("Austria", "Die Oesterreichische Bibliothekenverbund und Service"),
                      ("Austria", "Bundesforschungs und Ausbildungszentrum für Wald, Naturgefahren und Landschaft"),
                      ("Austria", "Donauuniversität Krems"),
                      ("Austria", "Fachhochschule Campus Wien"),
                      ("Austria", "Fachhochschule Joanneum"),
                      ("Austria", "Fachhochschule Krems"),
                      ("Austria", "Fachhochschule Kärnten"),
                      ("Austria", "Fachhochschule Oberösterreich"),
                      ("Austria", "Fachhochschule St. Pölten"),
                      ("Austria", "Fachhochschule Vorarlberg"),
                      ("Austria", "Fachhochschule Wiener Neustadt"),
                      ("Austria", "Forschungsinstitut für Molekulare Pathologie (IMP)"),
                      ("Austria", "Institut für Höhere Studien (IHS)"),
                      ("Austria", "Institute of Science and Technology Austria (I.S.T.)"),
                      ("Austria", "International Institute of Applied System Analysis (IIASA)"),
                      ("Austria", "Medizinische Universität Graz"),
                      ("Austria", "Medizinische Universität Wien"),
                      ("Austria", "Montanuniversität Leoben"),
                      ("Austria", "Paracelsus Medizinische Privatuniversität Salzburg"),
                      ("Austria", "Technische Universität Graz"),
                      ("Austria", "Technische Universität Wien"),
                      ("Austria", "Universität Graz"),
                      ("Austria", "Universität Klagenfurt"),
                      ("Austria", "Universität Linz"),
                      ("Austria", "Universität Salzburg"),
                      ("Austria", "Universität Wien"),
                      ("Austria", "Universität für Bodenkultur Wien"),
                      ("Austria", "Universitäts und Landesbibliothek Tirol"),
                      ("Austria", "Veterinärmedizinische Universität Wien"),
                      ("Austria", "Vorarlberger Landesbibliothek"),
                      ("Austria", "Wirtschaftsuniversität Wien"),
                      ("Belgium", "The Belgian Delegation"),
                      ("Belgium", "Consortium ELEKTRON"),
                      ("Belgium", "Katholieke Universiteit Leuven"),
                      ("Belgium", "Université Catholique de Louvain"),
                      ("Belgium", "Université de Liège"),
                      ("Belgium", "Université de Mons"),
                      ("Belgium", "Université de Namur (formerly Facultés Notre Dame de la Paix)"),
                      ("Belgium", "Université Libre de Bruxelles"),
                      ("Belgium", "Universiteit Antwerpen"),
                      ("Belgium", "Universiteit Gent"),
                      ("Belgium", "Vrije Universiteit Brussels"),
                      ("Canada", "The Canadian Research Knowledge Network"),
                      ("Canada", "Consortium CRKN"),
                      ("Canada", "Dalhousie University"),
                      ("Canada", "McGill University"),
                      ("Canada", "McMaster University"),
                      ("Canada", "Queen's University"),
                      ("Canada", "Simon Fraser University"),
                      ("Canada", "University of Alberta"),
                      ("Canada", "University of British Columbia"),
                      ("Canada", "University of Manitoba"),
                      ("Canada", "University of Regina"),
                      ("Canada", "University of Saskatchewan"),
                      ("Canada", "University of Toronto"),
                      ("Canada", "University of Victoria"),
                      ("Canada", "University of Waterloo"),
                      ("Canada", "Université Laval"),
                      ("Canada", "Université de Montréal"),
                      ("Canada", "Université de Sherbrooke"),
                      ("Canada", "Western University"),
                      ("Canada", "York University"),
                      ("China", "The National Science and Technology Library"),
                      ("China", "China Academy of Agricultural Sciences"),
                      ("China", "China Geological Library"),
                      ("China", "China Meteorological Administration"),
                      ("China", "Chinese Academy of Fishery Sciences"),
                      ("China", "Chinese Academy of Meidical Sciences"),
                      ("China", "DRAA SLCC National Consortium"),
                      ("China", "DRAA SLCC Regional Consortium"),
                      ("China", "Institute of Scientific and Technical Information of China"),
                      ("China", "State Intellectual Property Office of P.R.C"),
                      ("Czech Republic", "The National Library of Technology"),
                      ("Czech Republic", "Czech Springer Consortium"),
                      ("Czech Republic", "Ceské vysoké ucení technické v Praze"),
                      ("Czech Republic", "Consortium CZ.1.05/3.2.00/12.0228 - Natura: vedecké informacní zdroje prírodních ved"),
                      ("Czech Republic", "Fyzikální ústav AV CR, v.v.i."),
                      ("Czech Republic", "Národní technická knihovna"),
                      ("Czech Republic", "Slezská univerzita v Opave"),
                      ("Czech Republic", "Univerzita Karlova v Praze, Matematicko-fyzikální fakulta"),
                      ("Czech Republic", "Univerzita Pardubice"),
                      ("Czech Republic", "Vysoká skola chemicko-technologická v Praze"),
                      ("Czech Republic", "Ústav jaderné fyziky AV CR, v.v.i."),
                      ("Czech Republic", "Ústav organické chemie a biochemie AV CR, v.v.i."),
                      ("Czech Republic", "Ústav prístrojové techniky AV CR, v.v.i."),
                      ("Czech Republic", "Ústav termomechaniky AV CR, v.v.i."),
                      ("Denmark", "Danish Agency For Culture"),
                      ("Denmark", "Consortium DEFF"),
                      ("Finland", "The National Library of Finland"),
                      ("Finland", "FinElib consortium"),
                      ("Finland", "Aalto University"),
                      ("Finland", "Jyväskylä University"),
                      ("Finland", "University of Oulu"),
                      ("Finland", "Lappeenranta University of Technology"),
                      ("Finland", "Tampere University of Technology"),
                      ("Finland", "Helsinki University"),
                      ("Finland", "Turku University"),
                      ("France", "Centre National de la Recherche Scientifique"),
                      ("France", "CEA"),
                      ("France", "CNAM (Conservatoire national des arts et métiers)"),
                      ("France", "CNRS/IAS (Institut Astrophysique de Paris)"),
                      ("France", "Consortium CNRS"),
                      ("France", "Joint ILL-ESRF Library"),
                      ("France", "OBSPM (Observatoire de Paris-Meudon)"),
                      ("France", "Paris 6 - UPMC (SCD)"),
                      ("France", "Université Claude Bernard Lyon 1 (SCD)"),
                      ("France", "Université François Rabelais Tours (SCD)"),
                      ("France", "Université Grenoble 1"),
                      ("France", "Université Lille 1 Sciences et Technologies (SCD)"),
                      ("France", "Université Paul Sabatier - Toulouse 3 (SCD)"),
                      ("France", "Université de Bordeaux 1 (SCD)"),
                      ("France", "Université de Nantes"),
                      ("France", "Université de Poitiers (SCD)"),
                      ("France", "Université de Strasbourg (SCD)"),
                      ("France", "École Polytechnique Palaiseau (RNBM)"),
                      ("Germany", "Max Planck Digital Library"),
                      ("Germany", "Technische Informationsbibliothek"),
                      ("Germany", "Aachen - RWTH (Rheinisch-Westfälische Technische Hochschule) Aachen - Hochschulbibliothek"),
                      ("Germany", "Aachen - RWTH (Rheinisch-Westfälische Technische Hochschule) Aachen - Physikbibliothek"),
                      ("Germany", "Berlin HU - Humboldt-Universität zu Berlin - Universitätsbibliothek"),
                      ("Germany", "Bielefeld - Universität Bielefeld - Universitätsbibliothek"),
                      ("Germany", "Bochum - Ruhr-Universität - Universitätsbibliothek"),
                      ("Germany", "Bonn - Rheinische Friedrich-Wilhelms-Universität - Universitäts- und Landesbibliothek"),
                      ("Germany", "Bremen - Staats- und Universitätsbibliothek"),
                      ("Germany", "Darmstadt - Technische Universität - Universitäts- und Landesbibliothek"),
                      ("Germany", "Dortmund - Technische Universität - Universitätsbibliothek"),
                      ("Germany", "Dresden - SLUB (Sächsische Landesbibliothek - Staats- und Universitätsbibliothek)"),
                      ("Germany", "Erlangen-Nürnberg - FAU (Friedrich-Alexander-Universität) - Universitätsbibliothek"),
                      ("Germany", "Frankfurt am Main - Goethe-Universität Frankfurt am Main - Universitätsbibliothek Johann Christian Senckenberg"),
                      ("Germany", "Freiburg - Albert-Ludwigs-Universität - Universitätsbibliothek"),
                      ("Germany", "Gießen - Justus-Liebig-Universität - Universitätsbibliothek"),
                      ("Germany", "Göttingen - Niedersächsische Staats - und Universitätsbibliothek"),
                      ("Germany", "Hamburg - MIN-Fakultät - Fachbereich Physik"),
                      ("Germany", "Hamburg SUB - Staats- und Universitätsbibliothek Hamburg Carl von Ossietzky"),
                      ("Germany", "Hannover - Technische Informationsbibliothek (TIB) Hannover"),
                      ("Germany", "HeBis Consortium - all libraries - alle Bibliotheken"),
                      ("Germany", "Heidelberg - Ruprecht-Karls-Universität - Universitätsbibliothek"),
                      ("Germany", "Karlsruhe KIT - Karlsruher Institut für Technologie - KIT- Bibliothek"),
                      ("Germany", "Mainz - Johannes Gutenberg-Universität - Universitätsbibliothek"),
                      ("Germany", "München LMU - Ludwig-Maximilians-Universität - Universitätsbibliothek"),
                      ("Germany", "München TUM - Technische Universität München - Universitätsbibliothek"),
                      ("Germany", "Münster - Westfälische Wilhelms-Universität - Universitäts- und Landesbibliothek"),
                      ("Germany", "Oldenburg - Carl von Ossietzky Universität Oldenburg - BIS - Bibliotheks- und Informationssystem - Universitätsbibliothek"),
                      ("Germany", "Potsdam - Universität Potsdam - Universitätsbibliothek"),
                      ("Germany", "Regensburg - Universität Regensburg - Universitätsbibliothek"),
                      ("Germany", "Rostock - Universität Rostock - Universitätsbibliothek"),
                      ("Germany", "Siegen - Universität Siegen - Universitätsbibliothek"),
                      ("Germany", "Würzburg - Julius-Maximilians-Universität Würzburg  - Universitätsbibliothek"),
                      ("Germany", "HGF - Deutsches Elektronen-Synchrotron DESY"),
                      ("Germany", "HGF - Forschungszentrum Jülich"),
                      ("Germany", "HGF - GSI Helmholtzzentrum für Schwerionenforschung"),
                      ("Germany", "HGF - Helmholtz-Zentrum Dresden-Rossendorf"),
                      ("Germany", "HGF - Helmholtz-Zentrum Potsdam - Deutsches GeoForschungsZentrum GFZ"),
                      ("Greece", "HEAL-Link Consortium"),
                      ("Hong-Kong", "Joint University Librarians Advisory Committee (JULAC)"),
                      ("Hong-Kong", "Chinese University of Hong Kong"),
                      ("Hong-Kong", "City University of Hong Kong"),
                      ("Hong-Kong", "Hong Kong Institute of Education"),
                      ("Hong-Kong", "Hong Kong Polytechnic University"),
                      ("Hong-Kong", "Hong Kong University of Science & Technology"),
                      ("Hong-Kong", "Open University of Hong Kong"),
                      ("Hong-Kong", "University of Hong Kong"),
                      ("Hungary", "The Library and Information Centre of the Hungarian Academy of Sciences"),
                      ("Hungary", "EISZ Consortium1"),
                      ("Hungary", "Institute of Nuclear Research, HAS"),
                      ("Hungary", "Wigner Research Centre for Physics, HAS"),
                      ("Italy", "Istituto Nazionale Fisica Nucleare"),
                      ("Italy", "CNR Library"),
                      ("Italy", "ENEA library"),
                      ("Italy", "ICTP - Trieste"),
                      ("Italy", "INFN LN Frascati"),
                      ("Italy", "INFN LN Gran Sasso"),
                      ("Italy", "INFN LN Legnaro"),
                      ("Italy", "INFN LN Sud"),
                      ("Italy", "Istituto S.Anna Pisa"),
                      ("Italy", "Politecnico di Torino"),
                      ("Italy", "Politecnico Milano"),
                      ("Italy", "Scuola Normale Pisa"),
                      ("Italy", "Sincrotrone Trieste"),
                      ("Italy", "SISSA Trieste"),
                      ("Italy", "Università Cattolica del Sacro Cuore"),
                      ("Italy", "Università del Salento"),
                      ("Italy", "Università della Calabria"),
                      ("Italy", "Università dell'Aquila"),
                      ("Italy", "Università dell'Insubria"),
                      ("Italy", "Università di Bari"),
                      ("Italy", "Università di Bologna"),
                      ("Italy", "Università di Brescia"),
                      ("Italy", "Università di Cagliari"),
                      ("Italy", "Università di Catania"),
                      ("Italy", "Università di Ferrara"),
                      ("Italy", "Università di Firenze"),
                      ("Italy", "Università di Genova"),
                      ("Italy", "Università di Milano Statale"),
                      ("Italy", "Università di Milano-Bicocca"),
                      ("Italy", "Università di Modena e Reggio"),
                      ("Italy", "Università di Napoli Federico II"),
                      ("Italy", "Università di Padova"),
                      ("Italy", "Università di Palermo"),
                      ("Italy", "Università di Pavia"),
                      ("Italy", "Università di Perugia"),
                      ("Italy", "Università di Pisa"),
                      ("Italy", "Università di Roma La Sapienza"),
                      ("Italy", "Università di Salerno"),
                      ("Italy", "Università di Torino"),
                      ("Italy", "Università di Trento"),
                      ("Italy", "Università di Trieste"),
                      ("Italy", "Università di Udine"),
                      ("Italy", "Università Roma Tre"),
                      ("Japan", "The National Institute of Informatics"),
                      ("Japan", "Aoyama Gakuin University Library"),
                      ("Japan", "Chiba University Library"),
                      ("Japan", "High Energy Accelerator Research Organization Library"),
                      ("Japan", "Hiroshima University Library"),
                      ("Japan", "Hokkaido University Library"),
                      ("Japan", "Ibaraki University Library"),
                      ("Japan", "Institute of Space and Astronautical Science Library"),
                      ("Japan", "International Christian University Library"),
                      ("Japan", "Keio University Media Center"),
                      ("Japan", "Kobe University Library"),
                      ("Japan", "Kumamoto University Library"),
                      ("Japan", "Kwansei Gakuin University Library"),
                      ("Japan", "Kyoto University Library"),
                      ("Japan", "Kyushu Institute of Technology Library"),
                      ("Japan", "Kyushu University Library"),
                      ("Japan", "Meiji University Library"),
                      ("Japan", "Nagoya Institute of Technology Library"),
                      ("Japan", "Nagoya University Library"),
                      ("Japan", "National Institute of Informatics Library"),
                      ("Japan", "Niigata University Library"),
                      ("Japan", "Nihon University Library"),
                      ("Japan", "Osaka University Library"),
                      ("Japan", "RIKEN Library"),
                      ("Japan", "Rikkyo University Library"),
                      ("Japan", "Ritsumeikan University Library"),
                      ("Japan", "Shinshu University Library"),
                      ("Japan", "Tohoku University Library"),
                      ("Japan", "Tokai University Library"),
                      ("Japan", "Tokyo Institute of Technology Library"),
                      ("Japan", "Tokyo Woman's Christian University Library"),
                      ("Japan", "University of Tokyo Library System"),
                      ("Japan", "University of Tsukuba Library"),
                      ("Japan", "Waseda University Library"),
                      ("Japan", "Yamagata University Library"),
                      ("Armenia", "Joint Institute for Nuclear Research"),
                      ("Azerbaijan", "Joint Institute for Nuclear Research"),
                      ("Belarus", "Joint Institute for Nuclear Research"),
                      ("Cuba", "Joint Institute for Nuclear Research"),
                      ("North Korea", "Joint Institute for Nuclear Research"),
                      ("Georgia", "Joint Institute for Nuclear Research"),
                      ("Kazakhstan", "Joint Institute for Nuclear Research"),
                      ("Moldova", "Joint Institute for Nuclear Research"),
                      ("Mongolia ", "Joint Institute for Nuclear Research"),
                      ("Ukraine", "Joint Institute for Nuclear Research"),
                      ("Uzbekistan", "Joint Institute for Nuclear Research"),
                      ("Vietnam", "Joint Institute for Nuclear Research"),
                      ("South Korea", "Korea Institute of Science and Technology Information"),
                      ("South Korea", "Agency for Defense Development"),
                      ("South Korea", "Ajou University"),
                      ("South Korea", "Ajou University Medical Library"),
                      ("South Korea", "Andong National University"),
                      ("South Korea", "Animal, Plant and Fisheries Quarantine and Inspection Agency"),
                      ("South Korea", "CJ Cheiljedang Corporation."),
                      ("South Korea", "Catholic University College of Medicine"),
                      ("South Korea", "Catholic of Daegu School of Medicine"),
                      ("South Korea", "Changwon National University"),
                      ("South Korea", "Cheju National University"),
                      ("South Korea", "Cheongju University"),
                      ("South Korea", "Chonbuk National University"),
                      ("South Korea", "Chonnam National University"),
                      ("South Korea", "Chosun University"),
                      ("South Korea", "Chung-Ang University, Anseong Campus"),
                      ("South Korea", "Chungang University (Seoul)"),
                      ("South Korea", "Chungang University Medical Center"),
                      ("South Korea", "Chungbuk National University"),
                      ("South Korea", "Chungnam National University"),
                      ("South Korea", "Climate Research Lab"),
                      ("South Korea", "Daegu Gyeongbuk Institute of Science and Technology"),
                      ("South Korea", "Daejeon St. Mary's Hospital"),
                      ("South Korea", "Daejeon University"),
                      ("South Korea", "Daesang Corporation"),
                      ("South Korea", "Daewoong Co., Ltd."),
                      ("South Korea", "Dankook University Cheonan Campus"),
                      ("South Korea", "Dankook University Jukjeon Campus"),
                      ("South Korea", "Dong-A University"),
                      ("South Korea", "Dongduk Women's University"),
                      ("South Korea", "Dongguk University"),
                      ("South Korea", "Dongguk University Gyeongju Library"),
                      ("South Korea", "Dongseo University"),
                      ("South Korea", "Duksung Women's University"),
                      ("South Korea", "ETRI"),
                      ("South Korea", "Ewha Womans University"),
                      ("South Korea", "GaChon University (Global Campus)"),
                      ("South Korea", "GaChon University (Medical Campus)"),
                      ("South Korea", "Gangneung Wonju National University"),
                      ("South Korea", "Greenhouse Gas Inventory Research Center of Korea"),
                      ("South Korea", "Gwangju Institute of Science and Technology"),
                      ("South Korea", "Gyeongsang National University"),
                      ("South Korea", "Hallym University"),
                      ("South Korea", "Hanbat National University"),
                      ("South Korea", "Hankuk University of Foreign Studies Global Campus"),
                      ("South Korea", "Hanseo University"),
                      ("South Korea", "Hanyang University Seoul"),
                      ("South Korea", "Hongik University"),
                      ("South Korea", "Hoseo University Asan Campus"),
                      ("South Korea", "Hyundai Motor Company"),
                      ("South Korea", "Inha University"),
                      ("South Korea", "Inje University"),
                      ("South Korea", "Inje University Ilsan Paik Hospital"),
                      ("South Korea", "Inje University Medical Library"),
                      ("South Korea", "KERI"),
                      ("South Korea", "KFRI"),
                      ("South Korea", "KIAS"),
                      ("South Korea", "KICET"),
                      ("South Korea", "KIER"),
                      ("South Korea", "KIMM"),
                      ("South Korea", "KIPO"),
                      ("South Korea", "KIST"),
                      ("South Korea", "KITECH"),
                      ("South Korea", "KRRI"),
                      ("South Korea", "KT Corporate Technology Group"),
                      ("South Korea", "KT&G Central Research Institute"),
                      ("South Korea", "Kangbuk Samsung Hospital"),
                      ("South Korea", "Kangdong Sacred Heart Hospital"),
                      ("South Korea", "Kangnam University"),
                      ("South Korea", "Kangwon National University"),
                      ("South Korea", "Kongju National University"),
                      ("South Korea", "Konkuk University Chungju"),
                      ("South Korea", "Konkuk University Seoul"),
                      ("South Korea", "Kookmin University"),
                      ("South Korea", "Korea Advanced Institute of Science and Technology (KAIST)"),
                      ("South Korea", "Korea Aerospace University"),
                      ("South Korea", "Korea Astronomy and Space Science Institute"),
                      ("South Korea", "Korea Atomic Energy Research Institute"),
                      ("South Korea", "Korea Automotive Technology Institute"),
                      ("South Korea", "Korea Basic Science Institute"),
                      ("South Korea", "Korea Environment Institute"),
                      ("South Korea", "Korea Forest Research Institute"),
                      ("South Korea", "Korea Forest Seed & Variery Center"),
                      ("South Korea", "Korea Institute for Health and Social Affairs"),
                      ("South Korea", "Korea Institute of Atmospheric Prediction System (KIAPS)"),
                      ("South Korea", "Korea Institute of Construction Technology"),
                      ("South Korea", "Korea Institute of Geoscience and Mineral Resources"),
                      ("South Korea", "Korea Institute of Materials Science"),
                      ("South Korea", "Korea Institute of Ocean Science & Technology (KIOST)"),
                      ("South Korea", "Korea Institute of Radiological and Medical Sciences"),
                      ("South Korea", "Korea Maritime University"),
                      ("South Korea", "Korea Military Academy"),
                      ("South Korea", "Korea National Arboretum"),
                      ("South Korea", "Korea National University of Transportation"),
                      ("South Korea", "Korea Ocean Research and Development Institute (KORDI)"),
                      ("South Korea", "Korea Polytechnic University"),
                      ("South Korea", "Korea Research Institute of Bioscience & Biotechnology (KRIBB)"),
                      ("South Korea", "Korea Research Institute of Chemical Technology (KRICT)"),
                      ("South Korea", "Korea University Seoul"),
                      ("South Korea", "Korea Yakult"),
                      ("South Korea", "Kunsan National University"),
                      ("South Korea", "Kwangwoon University"),
                      ("South Korea", "Kyonggi University"),
                      ("South Korea", "Kyung Hee University Global campus"),
                      ("South Korea", "Kyung Hee University Hospital at Gangdong"),
                      ("South Korea", "Kyunghee University Medical Center"),
                      ("South Korea", "Kyunghee University Seoul"),
                      ("South Korea", "Kyungnam University"),
                      ("South Korea", "Kyungpook National University"),
                      ("South Korea", "Kyungsung University"),
                      ("South Korea", "LG Chemical Ltd."),
                      ("South Korea", "LG Display"),
                      ("South Korea", "LG Hausys"),
                      ("South Korea", "Mokwon University"),
                      ("South Korea", "Myongji University Science Campus"),
                      ("South Korea", "National Fisheries R&D"),
                      ("South Korea", "National Fusion Research Institute"),
                      ("South Korea", "National Institute for Mathematical Sciences"),
                      ("South Korea", "National Institute of Environmental Research"),
                      ("South Korea", "Paichai University"),
                      ("South Korea", "Patent Information Promotion Center"),
                      ("South Korea", "Pohang University of Science and Technology"),
                      ("South Korea", "Pukyong National University"),
                      ("South Korea", "Pusan National University"),
                      ("South Korea", "RIST"),
                      ("South Korea", "Rural Development Administration"),
                      ("South Korea", "Sahmyook University"),
                      ("South Korea", "Samsung Advanced Institut of Technology"),
                      ("South Korea", "Samsung Changwon Hospital"),
                      ("South Korea", "Samsung Digital City"),
                      ("South Korea", "Samsung Electro-Mechanics Co."),
                      ("South Korea", "Samsung Electronics Semiconductor"),
                      ("South Korea", "Sangji University"),
                      ("South Korea", "Sangmyung University Cheonan"),
                      ("South Korea", "Sejong University"),
                      ("South Korea", "Semyung University"),
                      ("South Korea", "Seoul National University"),
                      ("South Korea", "Seoul National University College of Medicine"),
                      ("South Korea", "Seoul National University of Science and Technology"),
                      ("South Korea", "Seoul Semiconductor LTD"),
                      ("South Korea", "Seoul Women's University"),
                      ("South Korea", "Sogang University"),
                      ("South Korea", "Sookmyung Women's University"),
                      ("South Korea", "Soonchunhyang University"),
                      ("South Korea", "Soonchunhyang University Hospital Seoul"),
                      ("South Korea", "Soongsil University"),
                      ("South Korea", "Sunchon University"),
                      ("South Korea", "SungKyunKwan University Natural Science Campus"),
                      ("South Korea", "The Catholic University of Korea"),
                      ("South Korea", "The Catholic University of Korea, Incheon St.Mary's Hospital"),
                      ("South Korea", "The University of Seoul"),
                      ("South Korea", "UNIST"),
                      ("South Korea", "University Ulsan College of Medicine Asan Medical Library"),
                      ("South Korea", "University of Incheon"),
                      ("South Korea", "University of Ulsan"),
                      ("South Korea", "Wonkwang University"),
                      ("South Korea", "World Institute of Kimchi"),
                      ("South Korea", "Yeungnam Univ. Medical Center"),
                      ("South Korea", "Yeungnam University"),
                      ("South Korea", "Yonsei University Medical Library"),
                      ("South Korea", "Yonsei University Seoul"),
                      ("South Korea", "Yonsei University Wonju"),
                      ("South Korea", "Yonsei University Wonju College of Medicine"),
                      ("South Korea", "Yuhan Research Institute"),
                      ("Mexico", "CONACYT-CONRICYT"),
                      ("Netherlands", "SURFmarket"),
                      ("Netherlands", "Koninklijke Bibliotheek"),
                      ("Netherlands", "National Instituut voor Subatomaire Fysica"),
                      ("Netherlands", "FOM-NIKHEF"),
                      ("Netherlands", "Technische Universiteit Delft"),
                      ("Netherlands", "Technische Universiteit Eindhoven"),
                      ("Netherlands", "UKB Consortium"),
                      ("Netherlands", "Universiteit Leiden"),
                      ("Netherlands", "Universiteit Twente"),
                      ("Netherlands", "Universiteit van Amsterdam"),
                      ("Norway", "CRIStin"),
                      ("Norway", "NTNU - Norwegian University of science and technology Library"),
                      ("Norway", "University of Bergen Library"),
                      ("Norway", "University of Oslo Library"),
                      ("Poland", "ICM University of Warsaw"),
                      ("Poland", "Adam Mickiewicz University"),
                      ("Poland", "AGH University of Science and Technology"),
                      ("Poland", "Bialystok University"),
                      ("Poland", "Electronic Materials Technology Institute - Poland"),
                      ("Poland", "Gdansk Technical University"),
                      ("Poland", "Gdansk University"),
                      ("Poland", "Institute of Electron Technology"),
                      ("Poland", "Instytut Fizyki Plazmy i Laserowej Mikrosyntezy"),
                      ("Poland", "Jagiellonian University - Krakow"),
                      ("Poland", "Jan Kochanowski University"),
                      ("Poland", "Koszalin Technical University"),
                      ("Poland", "Lodz University"),
                      ("Poland", "Marie Curie-Sklodowska University"),
                      ("Poland", "Military University of Technology"),
                      ("Poland", "Nicholas Copernicus University"),
                      ("Poland", "Polish Academy of Sciences - Henryka Niewodniczanskiego Institute of Nuclear Physics"),
                      ("Poland", "Polish Academy of Sciences - Institute of Fluid Flow Machinery"),
                      ("Poland", "Polish Academy of Sciences - Institute of Low Temperature and Structure Research"),
                      ("Poland", "Polish Academy of Sciences - Institute of Mathematics"),
                      ("Poland", "Polish Academy of Sciences - Institute of Molecular Physics"),
                      ("Poland", "Polish Academy of Sciences - Institute of Physical Chemistry"),
                      ("Poland", "Polish Academy of Sciences - Institute of Physics"),
                      ("Poland", "Poznan University of Technology"),
                      ("Poland", "Rzeszow University"),
                      ("Poland", "Silesia Technical University"),
                      ("Poland", "Silesia University - Katowice"),
                      ("Poland", "Szczecin University"),
                      ("Poland", "Warsaw University"),
                      ("Poland", "Warsaw University of Technology"),
                      ("Poland", "West Pomeranian University of Technology"),
                      ("Poland", "Wroclaw University"),
                      ("Poland", "Wroclaw University of Technology"),
                      ("Portugal", "Fundação Para a Ciência e a Tecnologia, I.P."),
                      ("Portugal", "b-on Consortium"),
                      ("Slovak Republic", "Ministry of Education, Science, Research and Sport of the Slovak Republic"),
                      ("South Africa", "South African National Library and Information Consortium"),
                      ("South Africa", "South African Astronomical Observatory (SAAO)"),
                      ("South Africa", "Stellenbosch University"),
                      ("South Africa", "University of Cape Town"),
                      ("South Africa", "University of KwaZulu-Natal"),
                      ("South Africa", "University of Pretoria"),
                      ("South Africa", "University of South Africa"),
                      ("South Africa", "University of Witwatersrand"),
                      ("South Africa", "University of the Western Cape"),
                      ("Spain", "Consorcio de Bibliotecas Universitarias de Andalucia (CBUA)"),
                      ("Spain", "Universidad de Cádiz"),
                      ("Spain", "Universidad de Granada"),
                      ("Spain", "Universidad de Huelva"),
                      ("Spain", "Universidad de Málaga"),
                      ("Spain", "Universidad de Navarra"),
                      ("Spain", "Universidad de Sevilla"),
                      ("Spain", "Consorcio de Bibliotecas Universitarias de Castilla y Leon (BUCLE)"),
                      ("Spain", "Universidad de Salamanca"),
                      ("Spain", "Universidad de Burgos"),
                      ("Spain", "Universidad de León"),
                      ("Spain", "Universidad de Valladolid"),
                      ("Spain", "Consorcio de Bibliotecas Universitarias de Galicia (BUGalicia)"),
                      ("Spain", "Universidade da Coruña"),
                      ("Spain", "Universidade de Santiago de Compostela"),
                      ("Spain", "Universidade de Vigo"),
                      ("Spain", "Consortium Canarias-Levante"),
                      ("Spain", "Universidad Miguel Hernández"),
                      ("Spain", "Universidad Politécnica de Cartagena"),
                      ("Spain", "Universidad Politécnica de Valencia"),
                      ("Spain", "Universidad de Alicante"),
                      ("Spain", "Universidad de Castilla-La Mancha"),
                      ("Spain", "Universidad de La Laguna"),
                      ("Spain", "Universidad de Las Palmas de Gran Canaria"),
                      ("Spain", "Universidad de Murcia"),
                      ("Spain", "Universidad de València"),
                      ("Spain", "Universidad de Extremadura"),
                      ("Spain", "Universidad Complutense"),
                      ("Spain", "Centro de Investigaciones Energeticas, Medioambientales y Tecnologicas (CIEMAT)"),
                      ("Spain", "Consejo Superior de Investigaciones Científicas (CSIC)"),
                      ("Spain", "Consorci de Serveis Universitaris de Catalunya (CSUC)"),
                      ("Spain", "Biblioteca de Catalunya"),
                      ("Spain", "Universitat Autònoma de Barcelona"),
                      ("Spain", "Universitat Jaume I"),
                      ("Spain", "Universitat Oberta de Catalunya"),
                      ("Spain", "Universitat Politècnica de Catalunya"),
                      ("Spain", "Universitat Pompeu Fabra"),
                      ("Spain", "Universitat Rovira i Virgili"),
                      ("Spain", "Universitat de Barcelona"),
                      ("Spain", "Universitat de Girona"),
                      ("Spain", "Universitat de Lleida"),
                      ("Spain", "Universitat de les Illes Balears"),
                      ("Spain", "Grupo 9 de Universidades"),
                      ("Spain", "Universidad Pública de Navarra"),
                      ("Spain", "Universidad de Cantabria"),
                      ("Spain", "Universidad de La Rioja"),
                      ("Spain", "Universidad de Oviedo"),
                      ("Spain", "Universidad de País Vasco/Euskal Herriko Unibertsitatea"),
                      ("Spain", "Universidad de Zaragoza"),
                      ("Spain", "Consorcio Madroño"),
                      ("Spain", "UNED"),
                      ("Spain", "Universidad Autónoma de Madrid"),
                      ("Spain", "Universidad Carlos III"),
                      ("Spain", "Universidad Politécnica de Madrid"),
                      ("Sweden", "National Library of Sweden"),
                      ("Sweden", "BIBSAM Consortium"),
                      ("Sweden", "Chalmers University of Technology"),
                      ("Sweden", "Lund University"),
                      ("Sweden", "Royal Institute of Technology"),
                      ("Sweden", "Stockholm University"),
                      ("Sweden", "Uppsala University"),
                      ("Switzerland", "Consortium of Swiss Academic Libraries"),
                      ("Switzerland", "BCU - Fribourg"),
                      ("Switzerland", "EPFL"),
                      ("Switzerland", "ETH Zurich"),
                      ("Switzerland", "Fachhochschulen"),
                      ("Switzerland", "Lib4RI"),
                      ("Switzerland", "UB Bern"),
                      ("Switzerland", "Universität Basel"),
                      ("Switzerland", "Universität Zurich"),
                      ("Switzerland", "Université de Genève"),
                      ("Turkey", "Turkish Academic Network and Information Center"),
                      ("Turkey", "Consortium TUBITAK ULAKBIM"),
                      ("United Kingdom", "JISC Collections"),
                      ("United Kingdom", "Aberystwyth University"),
                      ("United Kingdom", "Aston University"),
                      ("United Kingdom", "Bangor University"),
                      ("United Kingdom", "Biotechnology and Biological Sciences Research Council"),
                      ("United Kingdom", "Bournemouth University"),
                      ("United Kingdom", "Cranfield University"),
                      ("United Kingdom", "Edge Hill University"),
                      ("United Kingdom", "Edinburgh Napier University"),
                      ("United Kingdom", "Glasgow Caledonian University"),
                      ("United Kingdom", "Heriot-Watt University"),
                      ("United Kingdom", "Imperial College London"),
                      ("United Kingdom", "Institute of Education"),
                      ("United Kingdom", "Keele University"),
                      ("United Kingdom", "King's College London"),
                      ("United Kingdom", "Kingston University"),
                      ("United Kingdom", "Lancaster University"),
                      ("United Kingdom", "Leeds Metropolitan University"),
                      ("United Kingdom", "Liverpool John Moores University"),
                      ("United Kingdom", "London School of Economics"),
                      ("United Kingdom", "London South Bank University"),
                      ("United Kingdom", "Loughborough University"),
                      ("United Kingdom", "Manchester Metropolitan University"),
                      ("United Kingdom", "National Library of Scotland"),
                      ("United Kingdom", "Newcastle University"),
                      ("United Kingdom", "Northumbria University"),
                      ("United Kingdom", "Nottingham Trent University"),
                      ("United Kingdom", "Queen Margaret University, Edinburgh"),
                      ("United Kingdom", "Queen Mary & Westfield College"),
                      ("United Kingdom", "Queen's University Belfast"),
                      ("United Kingdom", "Reading University"),
                      ("United Kingdom", "Royal Holloway, University of London"),
                      ("United Kingdom", "Scotland's Rural College"),
                      ("United Kingdom", "Sheffield Hallam University"),
                      ("United Kingdom", "St George's University of London"),
                      ("United Kingdom", "STFC Chadwick & RAL Libraries incl STFC Roe Lib"),
                      ("United Kingdom", "Swansea University"),
                      ("United Kingdom", "The Open University"),
                      ("United Kingdom", "The Robert Gordon University"),
                      ("United Kingdom", "University College London"),
                      ("United Kingdom", "University College Suffolk"),
                      ("United Kingdom", "University of Aberdeen"),
                      ("United Kingdom", "University of Abertay"),
                      ("United Kingdom", "University of Bath"),
                      ("United Kingdom", "University of Birmingham"),
                      ("United Kingdom", "University of Bristol"),
                      ("United Kingdom", "University of Cambridge"),
                      ("United Kingdom", "University of Central Lancashire"),
                      ("United Kingdom", "University of Derby"),
                      ("United Kingdom", "University of Dundee"),
                      ("United Kingdom", "University of Durham"),
                      ("United Kingdom", "University of East Anglia"),
                      ("United Kingdom", "University of Edinburgh"),
                      ("United Kingdom", "University of Exeter"),
                      ("United Kingdom", "University of Glasgow"),
                      ("United Kingdom", "University of Hertfordshire"),
                      ("United Kingdom", "University of Huddersfield"),
                      ("United Kingdom", "University of Hull"),
                      ("United Kingdom", "University of Kent"),
                      ("United Kingdom", "University of Leeds"),
                      ("United Kingdom", "University of Leicester"),
                      ("United Kingdom", "University of Liverpool"),
                      ("United Kingdom", "University of Manchester Library"),
                      ("United Kingdom", "University of Northampton"),
                      ("United Kingdom", "University of Nottingham"),
                      ("United Kingdom", "University of Oxford"),
                      ("United Kingdom", "University of Salford"),
                      ("United Kingdom", "University of Sheffield"),
                      ("United Kingdom", "University of Southampton"),
                      ("United Kingdom", "University of St Andrews"),
                      ("United Kingdom", "University of Stirling"),
                      ("United Kingdom", "University of Strathclyde"),
                      ("United Kingdom", "University of Surrey"),
                      ("United Kingdom", "University of Sussex"),
                      ("United Kingdom", "University of the Highlands & Islands"),
                      ("United Kingdom", "University of the West of England"),
                      ("United Kingdom", "University of the West of Scotland"),
                      ("United Kingdom", "University of Ulster"),
                      ("United Kingdom", "University of Warwick"),
                      ("United Kingdom", "University of Westminster"),
                      ("United Kingdom", "University of York"),
                      ("United States", "California Digital Library"),
                      ("United States", "Lawrence Berkeley National Laboratory"),
                      ("United States", "Lawrence Livermore National Laboratory"),
                      ("United States", "Lyrasis"),
                      ("United States", "American University, Washington DC"),
                      ("United States", "Arizona State University"),
                      ("United States", "Auburn University"),
                      ("United States", "Baylor University"),
                      ("United States", "Boston College"),
                      ("United States", "Boston University"),
                      ("United States", "Brandeis University"),
                      ("United States", "Brigham Young University"),
                      ("United States", "Brown University"),
                      ("United States", "Cal State University (CSU)"),
                      ("United States", "Cal State University, Fresno"),
                      ("United States", "California Institute of Technology"),
                      ("United States", "Carnegie Mellon University"),
                      ("United States", "Claremont University Consortium"),
                      ("United States", "Columbia University"),
                      ("United States", "College of William and Mary"),
                      ("United States", "College of the Holy Cross"),
                      ("United States", "Colorado State University"),
                      ("United States", "Consortium - OhioLINK"),
                      ("United States", "Cornell University Library, Ithaca, NY"),
                      ("United States", "Creighton University"),
                      ("United States", "DOE Argonne National Laboratory"),
                      ("United States", "DOE Brookhaven National Laboratory"),
                      ("United States", "DOE Fermi National Accelerator Laboratory"),
                      ("United States", "DOE Los Alamos National Laboratory"),
                      ("United States", "DOE Oak Ridge National Laboratory"),
                      ("United States", "DOE Pacific Northwest National Laboratory"),
                      ("United States", "DOE SLAC National Accelerator Laboratory"),
                      ("United States", "DOE Thomas Jefferson National Accelerator Facility"),
                      ("United States", "Dartmouth College"),
                      ("United States", "Duke University"),
                      ("United States", "East Carolina University"),
                      ("United States", "Emory University"),
                      ("United States", "Florida Atlantic University"),
                      ("United States", "Florida Institute of technology"),
                      ("United States", "Florida International University"),
                      ("United States", "Florida State University"),
                      ("United States", "George Mason University"),
                      ("United States", "Georgetown University"),
                      ("United States", "Georgia Institute of Technology (GA Tech)"),
                      ("United States", "Georgia State University"),
                      ("United States", "Harvard University"),
                      ("United States", "Haverford College"),
                      ("United States", "Illinois Institute of Technology"),
                      ("United States", "Indiana University"),
                      ("United States", "Iowa State University"),
                      ("United States", "James Madison University"),
                      ("United States", "Johns Hopkins University"),
                      ("United States", "Kansas State University"),
                      ("United States", "Lafayette College"),
                      ("United States", "Louisiana State University"),
                      ("United States", "MCLS"),
                      ("United States", "Massachusetts Institute of Technology"),
                      ("United States", "Michigan State University"),
                      ("United States", "Montana State University"),
                      ("United States", "New York University"),
                      ("United States", "North Carolina State University"),
                      ("United States", "North Dakota State University"),
                      ("United States", "Northeastern University"),
                      ("United States", "Northwestern University"),
                      ("United States", "Pennsylvania State University"),
                      ("United States", "Princeton University"),
                      ("United States", "Purdue University"),
                      ("United States", "Rensselaer Polytechnic"),
                      ("United States", "Rice University"),
                      ("United States", "Rochester Institute of Technology"),
                      ("United States", "Rockefeller University"),
                      ("United States", "Rutgers University"),
                      ("United States", "Smith College"),
                      ("United States", "South Dakota State University"),
                      ("United States", "Southern Methodist University"),
                      ("United States", "Stony Brook University"),
                      ("United States", "Syracuse University"),
                      ("United States", "Temple University"),
                      ("United States", "Texas A & M"),
                      ("United States", "Texas Tech University"),
                      ("United States", "Trinity University, San Antonio TX"),
                      ("United States", "Tufts University"),
                      ("United States", "Tulane University"),
                      ("United States", "University at Buffalo, State University of New York"),
                      ("United States", "University of Alabama, Birmingham"),
                      ("United States", "University of Alabama, Huntsville"),
                      ("United States", "University of Alabama, Tuscaloosa"),
                      ("United States", "University of Arizona"),
                      ("United States", "University of Arkansas"),
                      ("United States", "University of Central Florida"),
                      ("United States", "University of Chicago"),
                      ("United States", "University of Colorado Boulder"),
                      ("United States", "University of Denver"),
                      ("United States", "University of Florida"),
                      ("United States", "University of Georgia"),
                      ("United States", "University of Idaho"),
                      ("United States", "University of Illinois, Chicago"),
                      ("United States", "University of Illinois, Urbana-Champaign"),
                      ("United States", "University of Iowa"),
                      ("United States", "University of Kansas"),
                      ("United States", "University of Kentucky"),
                      ("United States", "University of Maine, Bangor"),
                      ("United States", "University of Maryland Baltimore County"),
                      ("United States", "University of Maryland, College Park MD"),
                      ("United States", "University of Massachusetts, Amherst"),
                      ("United States", "University of Miami"),
                      ("United States", "University of Michigan, Ann Arbor"),
                      ("United States", "University of Minnesota"),
                      ("United States", "University of Mississippi"),
                      ("United States", "University of Missouri"),
                      ("United States", "University of Nebraska-Lincoln"),
                      ("United States", "University of New Mexico"),
                      ("United States", "University of North Carolina Charlotte"),
                      ("United States", "University of North Carolina, Chapel Hill"),
                      ("United States", "University of North Carolina, Greensboro"),
                      ("United States", "University of North Dakota"),
                      ("United States", "University of North Texas"),
                      ("United States", "University of Northern Iowa"),
                      ("United States", "University of Oklahoma"),
                      ("United States", "University of Oregon"),
                      ("United States", "University of Pennsylvania"),
                      ("United States", "University of Pittsburgh"),
                      ("United States", "University of Puerto Rico"),
                      ("United States", "University of Rhode Island"),
                      ("United States", "University of Rochester"),
                      ("United States", "University of South Alabama"),
                      ("United States", "University of South Carolina"),
                      ("United States", "University of Southern California"),
                      ("United States", "University of Tennessee, Knoxville"),
                      ("United States", "University of Texas, Arlington"),
                      ("United States", "University of Texas, Austin"),
                      ("United States", "University of Texas, San Antonio"),
                      ("United States", "University of Utah, Salt Lake City"),
                      ("United States", "University of Virginia"),
                      ("United States", "University of Washington"),
                      ("United States", "University of Wisconsin"),
                      ("United States", "University of Wyoming"),
                      ("United States", "Utah State University"),
                      ("United States", "VIVA"),
                      ("United States", "Valparaiso University"),
                      ("United States", "Vanderbilt University"),
                      ("United States", "Virginia Commonwealth University"),
                      ("United States", "Virginia Institute of Technology (VA Tech)"),
                      ("United States", "Wake Forest University"),
                      ("United States", "Washington State University"),
                      ("United States", "Washington University, Saint Louis"),
                      ("United States", "Wayne State University"),
                      ("United States", "Wellesley College"),
                      ("United States", "West Virginia University"),
                      ("United States", "Yeshiva University"))

    for institute in def_institutes:
        country_id = run_sql("SELECT id FROM country WHERE name = %s", (institute[0],))
        try:
            run_sql("INSERT INTO institution (name, country_id) VALUES(%s, %s)", (institute[1], country_id[0][0]))
        except Exception as e:
            print e

    return ""


def _prepare_country_db():
    return run_sql("""CREATE TABLE IF NOT EXISTS country (
        id mediumint NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL UNIQUE,
        PRIMARY KEY country(id)
    ) ENGINE=MyISAM;""")


def _prepare_registration_db():
    return run_sql("""CREATE TABLE IF NOT EXISTS registration (
        id mediumint NOT NULL AUTO_INCREMENT,
        email varchar(255) NOT NULL UNIQUE,
        name varchar(255) NOT NULL,
        position varchar(255) NOT NULL,
        country varchar(255),
        country_id mediumint,
        organisation varchar(255),
        organisation_id mediumint,
        is_affiliated boolean NOT NULL,
        description varchar(5000) NOT NULL,
        accepted boolean NOT NULL DEFAULT false,
        PRIMARY KEY registration(id),
        FOREIGN KEY (country_id)
            REFERENCES country(id)
            ON DELETE CASCADE,
        FOREIGN KEY (organisation_id)
            REFERENCES institution(id)
            ON DELETE CASCADE
    ) ENGINE=MyISAM;""")

def _prepare_institut_db():
    return run_sql("""CREATE TABLE IF NOT EXISTS institution (
        id mediumint NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL UNIQUE,
        country_id mediumint NOT NULL,
        PRIMARY KEY institution(id),
        FOREIGN KEY (country_id)
            REFERENCES country(id)
            ON DELETE CASCADE,
        KEY (name)
    ) ENGINE=MyISAM;""")


def get_countries(req):
    countries = run_sql("SELECT name, id from country ORDER BY name")
    req.content_type = "application/json"
    json.dump(countries, req)


def get_organisation(req, country_id=""):
    req.content_type = "application/json"
    if country_id:
        org = run_sql("SELECT id, name FROM institution WHERE country_id = %s ORDER BY name", (country_id,))
        json.dump(org, req)


def _register(req, query_string, params, email):
    if not run_sql("SELECT id FROM registration WHERE email=%s", (email,)):
        try:
            run_sql(query_string, params)
            header = ""
            footer = """Best regards
                     The SCOAP3 team"""
            subject = "Registration to SCOAP3 API"
            content = "Thanks for your interest in the SCOAP3 API. We have received your request for a token. We will be back to you within one working day."
            send_email("info@scoap3.org", email, subject=subject, content=content, header=header, footer=footer)
            redirect_to_url(req, "http://api.scoap3.org/registered")
        except:
            redirect_to_url(req, "http://api.scoap3.org/registration_error")
    else:
        # emial already registered
        redirect_to_url(req, "http://api.scoap3.org/already_registered")


def register_associated(req, name, email, position, country, organisation):
    query_string = """INSERT INTO registration(name, email, position, country, organisation, is_affiliated) VALUES(%s, %s, %s, %s, %s, 1)"""
    params = (name, email, position, country, organisation)

    _register(req, query_string, params, email)


def register_not_associated(req, name, email, position, country, organisation, description):
    query_string = """INSERT INTO registration(name, email, position, country, organisation, is_affiliated, description) VALUES(%s, %s, %s, %s, %s, 0, %s)"""
    params = (name, email, position, country, organisation, description)

    _register(req, query_string, params, email)


def registration_admin(req, message=""):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return redirect_to_url(req, "http://api.scoap3.org")

    req.content_type = "text/html"
    req.write(pageheaderonly("Registration admin", req=req))

    if message:
        req.write("<strong>%s</strong>" % (message,))
    req.write("<h1>Registration list</h1>")

    regs = run_sql("SELECT * FROM registration", with_dict=True)

    req.write("<table>")
    req.write("<thead><tr><th>ID</th><th>Registration date</th><th>Name</th><th>Email</th><th>Position</th><th>Country</th><th>Organisation</th><th>Affiliated?</th><th>Desc.</th><th>Is accepted</th></tr>")
    count = 1
    for reg in regs:
        try:
            int(reg['country'])
            country = run_sql("Select name from country where id=%s", (reg['country'],))[0][0]
        except:
            country = reg['country']
        try:
            int(reg['organisation'])
            org = run_sql("Select name from institution where id=%s", (reg['organisation'],))[0][0]
        except:
            org = reg['organisation']

        key = ""
        if reg['is_accepted']:
            try:
                user_id = run_sql("Select id from user where email=%s", (reg['email'],), with_dict=True)[0]['id']
                key = _get_user_keys(user_id)['id']
            except:
                key = "Error"

        req.write("<tr>")
        req.write("<td>%(id)s</td><td>%(date)s</td><td>%(name)s</td><td>%(email)s</td><td>%(position)s</td><td>%(country)s</td><td>%(org)s</td><td>%(is_aff)s</td><td>%(desc)s</td>"
                  % {'id': count,
                     'date': reg['created'],
                     'name': reg['name'],
                     'email': reg['email'],
                     'position': reg['position'],
                     'country': country,
                     'org': org,
                     'is_aff': 'Yes' if reg['is_affiliated'] else 'No',
                     'desc': reg['description']})
        if not reg['is_accepted']:
            req.write("<td><a href='/api.py/accept_registration?registration_id=%(id)s'>Accept</a>" % {'id': reg['id']})
        else:
            req.write("<td>Yes: %s" % (key))
        req.write(" <a href='/api.py/delete_registration?registration_id=%(id)s'>Delete</a></td>" % {'id': reg['id']})
        req.write("</tr>")
        count += 1
    req.write("</table>")

    req.write(pagefooteronly(req=req))
    return ""


def _get_user_keys(user_id):
    latest_key = run_sql("SELECT id, secret FROM webapikey WHERE id_user=%s", (user_id,), with_dict=True)[-1]
    return latest_key


def accept_registration(req, registration_id):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return redirect_to_url(req, "http://api.scoap3.org")

    message = ''
    if registration_id:
        registration = run_sql("SELECT * from registration where id=%s", (registration_id,), with_dict=True)[0]
        # Creating user if not exist
        user_id = run_sql("Select id from user where email=%s", (registration['email'],), with_dict=True)
        if user_id:
            user_id = user_id[0]['id']
            message = "Email %s is already registered. Creating new API key.<br>" % (registration['email'],)
        else:
            user_id = run_sql("INSERT INTO user (email, password, note) values(%s ,AES_ENCRYPT(email,'inspire_scoap3'), '1')", (registration['email'],))
        # Crearing API keys
        create_new_web_api_key(user_id, "api")
        # sending email
        keys = _get_user_keys(user_id)
        email_content = """
Hi,<br>
<br>
Thank you for registering. Please find you API keys below. Remember that you should never share you private key with anyone. SCOAP3 support will never ask you for it.<br>
<br>
public key: %(public)s<br>
private key: %(private)s<br>
<br>
Documentation on how to use API can be found at <a href='http://scoap3.org/scoap3-repository/xml-api#key'>SCOAP3 XML API</a>.<br>
<br>
In case of problems do not hesitate to contact us.<br>
<br>
​Best regards,<br>
    SCOAP3 team
""" % {'public': keys['id'], 'private': keys['secret']}

        try:
            send_email("info@scoap3.org",
                       registration['email'],
                       subject="SCOAP3 Repository API key",
                       html_content=email_content,
                       header='',
                       footer='',
                       html_header='',
                       html_footer='',
                       bccaddr='repo.admin@scoap3.org')
            message += "The registration for %s was accepted." % (registration['email'],)
            run_sql("update registration set is_accepted=1 where id=%s", (registration_id,))
        except:
            message += "Failed to send email to the %s!" % (registration['email'],)
    else:
        message += "You need to specify registration ID."

    return redirect_to_url(req, "http://api.scoap3.org/api.py/registration_admin?message=%s" % (message,))


def delete_registration(req, registration_id):
    user_info = collect_user_info(req)
    if not acc_is_user_in_role(user_info, acc_get_role_id("SCOAP3")):
        return redirect_to_url(req, "http://api.scoap3.org")

    message = ''
    if registration_id:
        registration = run_sql("SELECT * from registration where id=%s", (registration_id,), with_dict=True)[0]
        user_id = run_sql("Select id from user where email=%s", (registration['email'],), with_dict=True)

        # check number of webapikeys
        try:
            webapikeys = run_sql("Select * from webapikey where id_user=%s", (user_id[0]['id'],), with_dict=True)
        except:
            webapikeys = []

        if len(webapikeys) > 1:  # if more than one apikey than do not do anything just inform the user (very unlikely)
            message += "There is more than one API key registered with: %s! Nothing was removed." % (registration['email'],)
        elif len(webapikeys) == 0:
            run_sql("DELETE from registration where id=%s", (registration_id,), with_dict=True)
            message += "User data and API key associated with: %s were deleted." % (registration['email'],)
        else:  # if one registration
            run_sql("DELETE from webapikey where id_user=%s", (user_id[0]['id'],), with_dict=True)
            run_sql("DELETE from user where id=%s", (user_id[0]['id'],), with_dict=True)
            run_sql("DELETE from registration where id=%s", (registration_id,), with_dict=True)
            message += "User data and API key associated with: %s were deleted." % (registration['email'],)
    else:
        message += "You need to specify registration ID."

    return redirect_to_url(req, "http://api.scoap3.org/api.py/registration_admin?message=%s" % (message,))
