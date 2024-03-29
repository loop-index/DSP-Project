import pandas as pd

# regions = pd.read_csv("ipinyou/region.en.txt", sep='\t', header=None)
# regions = regions.set_index(0)[1].to_dict()
# print(regions)

# cities = pd.read_csv("ipinyou/city.en.csv", header=None)
# cities = cities.set_index(0)[1].to_dict()
# print(cities)

# usertags = pd.read_csv("ipinyou/user.profile.tags.en.txt", sep='\t', header=None)
# usertags = usertags.set_index(0)[1].to_dict()
# print(usertags)

region_dict = {0: 'unknown', 1: 'beijing', 2: 'tianjin', 3: 'hebei', 15: 'shanxi', 27: 'neimenggu', 40: 'liaoning', 55: 'jilin', 65: 'heilongjiang', 79: 'shanghai', 80: 'jiangsu', 94: 'zhejiang', 106: 'anhui', 124: 'fujian', 134: 'jiangxi', 146: 'shandong', 164: 'henan',
               183: 'hubei', 201: 'hunan', 216: 'guangdong', 238: 'guangxi', 253: 'hainan', 275: 'chongqing', 276: 'sichuan', 298: 'guizhou', 308: 'yunnan', 325: 'xizang', 333: 'shannxi', 344: 'gansu', 359: 'qinghai', 368: 'ningxia', 374: 'xinjiang', 393: 'taiwan', 394: 'xianggang', 395: 'aomen'}

cities_dict = {0: 'unknown', 4: 'shijiazhuang', 5: 'tangshan', 6: 'qinhuangdao', 7: 'handan', 8: 'xingtai', 9: 'baoding', 10: 'zhangjiakou', 11: 'chengde', 12: 'cangzhou', 13: 'langfang', 14: 'hengshui', 16: 'taiyuan', 17: 'datong', 18: 'yangquan', 19: 'changzhi', 20: 'jincheng', 21: 'shuozhou', 
               22: 'jinzhongshi', 23: 'yuncheng', 24: 'xinzhou', 25: 'linfen', 26: 'lvliang', 28: 'huhehaote', 29: 'baotou', 30: 'wuhai', 31: 'chifeng', 32: 'tongliao', 33: 'eerduosi', 34: 'hulunbeier', 35: 'bayannaoer', 36: 'wulanchabu', 37: 'xingan', 38: 'xilinguole', 39: 'alashan', 41: 'shenyang', 
               42: 'dalian', 43: 'anshan', 44: 'fushun', 45: 'benxi', 46: 'dandong', 47: 'jinzhou', 48: 'yingkou', 49: 'fuxin', 50: 'liaoyang', 51: 'panjin', 52: 'tieling', 53: 'chaoyang', 54: 'huludao', 56: 'changchun', 57: 'jilin_city', 58: 'siping', 59: 'liaoyuan', 60: 'tonghua', 61: 'baishan', 
               62: 'songyuan', 63: 'baicheng', 64: 'yanbian', 66: 'haerbin', 67: 'qiqihaer', 68: 'jixi', 69: 'hegang', 70: 'shuangyashan', 71: 'daqing', 72: 'yichun_65', 73: 'jiamusi', 74: 'qitaihe', 75: 'mudanjiang', 76: 'heihe', 77: 'suihua', 78: 'daxinganling', 81: 'nanjing', 82: 'wuxi', 83: 'xuzhou', 
               84: 'changzhou', 85: 'suzhou_jiangsu', 86: 'nantong', 87: 'lianyungang', 88: 'huaian', 89: 'yancheng', 90: 'yangzhou', 91: 'zhenjiang', 92: 'taizhou_jiangsu', 93: 'suqian', 95: 'hangzhou', 96: 'ningbo', 97: 'wenzhou', 98: 'jiaxing', 99: 'huzhou', 100: 'shaoxing', 101: 'jinhua', 102: 'quzhou', 
               103: 'zhoushan', 104: 'taizhou', 105: 'lishui', 107: 'hefei', 108: 'wuhu', 109: 'bangbu', 110: 'huainan', 111: 'maanshan', 112: 'huaibei', 113: 'tongling', 114: 'anqing', 115: 'huangshan', 116: 'chuzhou', 117: 'fuyang', 118: 'suzhou', 119: 'chaohu', 120: 'liuan', 121: 'bozhou', 122: 'chizhou', 
               123: 'xuancheng', 125: 'fuzhou_124', 126: 'xiamen', 127: 'putian', 128: 'sanming', 129: 'quanzhou', 130: 'zhangzhou', 131: 'nanping', 132: 'longyan', 133: 'ningde', 135: 'nanchang', 136: 'jingdezhen', 137: 'pingxiang', 138: 'jiujiang', 139: 'xinyu', 140: 'yingtan', 141: 'ganzhou', 142: 'jian', 
               143: 'yichun_134', 144: 'fuzhou_134', 145: 'shangrao', 147: 'jinan', 148: 'qingdao', 149: 'zibo', 150: 'zaozhuang', 151: 'dongying', 152: 'yantai', 153: 'weifang', 154: 'jining', 155: 'taian', 156: 'weihai', 157: 'rizhao', 158: 'laiwu', 159: 'linyi', 160: 'dezhou', 161: 'liaocheng', 162: 'binzhou', 
               163: 'heze', 165: 'zhengzhou', 166: 'kaifeng', 167: 'luoyang', 168: 'pingdingshan', 169: 'anyang', 170: 'hebi', 171: 'xinxiang', 172: 'jiaozuo', 173: 'puyang', 174: 'xuchang', 175: 'luohe', 176: 'sanmenxia', 177: 'nanyang', 178: 'shangqiu', 179: 'xinyang', 180: 'zhoukou', 181: 'zhumadian', 
               182: 'jiyuan', 184: 'wuhan', 185: 'huangshi', 186: 'shiyan', 187: 'yichang', 188: 'xiangfan', 189: 'ezhou', 190: 'jingmen', 191: 'xiaogan', 192: 'jingzhou', 193: 'huanggang', 194: 'xianning', 195: 'suizhou', 196: 'enshishi', 197: 'xiantao', 198: 'qianjiang',
               199: 'tianmen', 200: 'shennongjia', 202: 'changsha', 203: 'zhuzhou', 204: 'xiangtan', 205: 'hengyang', 206: 'shaoyang', 207: 'yueyang', 208: 'changde', 209: 'zhangjiajie', 210: 'yiyang', 211: 'chenzhou', 212: 'yongzhou', 213: 'huaihua', 214: 'loudi', 215: 'xiangxi', 217: 'guangzhou', 
               218: 'shaoguan', 219: 'shenzhen', 220: 'zhuhai', 221: 'shantou', 222: 'foshan', 223: 'jiangmen', 224: 'zhanjiang', 225: 'maoming', 226: 'zhaoqing', 227: 'huizhou', 228: 'meizhou', 229: 'shanwei', 230: 'heyuan', 231: 'yangjiang', 232: 'qingyuan', 233: 'dongguan', 234: 'zhongshan', 235: 'chaozhou', 
               236: 'jieyang', 237: 'yunfu', 239: 'nanning', 240: 'liuzhou', 241: 'guilin', 242: 'wuzhou', 243: 'beihai', 244: 'fangchenggang', 245: 'qinzhou', 246: 'guigang', 247: 'yulin_238', 248: 'baise', 249: 'hezhou', 250: 'hechi', 251: 'laibin', 252: 'chongzuo', 254: 'haikou', 255: 'sanya', 256: 'wuzhishan', 
               257: 'qionghai', 258: 'danzhou', 259: 'wenchang', 260: 'wanning', 261: 'dongfang', 262: 'dingan', 263: 'tunchang', 264: 'chengmai', 265: 'lingao', 266: 'baisha', 267: 'changjiang', 268: 'ledong', 269: 'lingshui', 270: 'baoting', 271: 'qiongzhong', 272: 'xisha', 273: 'nansha', 274: 'zhongsha', 
               277: 'chengdu', 278: 'zigong', 279: 'panzhihua', 280: 'luzhou', 281: 'deyang', 282: 'mianyang', 283: 'guangyuan', 284: 'suining', 285: 'neijiang', 286: 'leshan', 287: 'nanchong', 288: 'meishan', 289: 'yibin', 290: 'guangan', 291: 'dazhou', 292: 'yaan', 293: 'bazhong', 294: 'ziyang', 295: 'aba', 
               296: 'ganzi', 297: 'liangshan', 299: 'guiyang', 300: 'liupanshui', 301: 'zunyi', 302: 'anshun', 303: 'tongren', 304: 'qianxinan', 305: 'bijie', 306: 'qiandongnan', 307: 'qiannan', 309: 'kunming', 310: 'qujing', 311: 'yuxi', 312: 'baoshan', 313: 'zhaotong', 314: 'lijiang', 315: 'puer', 316: 'lincang', 
               317: 'chuxiong', 318: 'honghe', 319: 'wenshan', 320: 'xishuangbanna', 321: 'dali', 322: 'dehong', 323: 'nujiang', 324: 'diqing', 326: 'lasa', 327: 'changdu', 328: 'shannan', 329: 'rikaze', 330: 'naqu', 331: 'ali', 332: 'linzhi', 334: 'xian', 335: 'tongzhou', 336: 'baoji', 337: 'xianyang', 338: 'weinan', 
               339: 'yanan', 340: 'hanzhong', 341: 'yulin_333', 342: 'ankang', 343: 'shangluo', 345: 'lanzhou', 346: 'jiayuguan', 347: 'jinchang', 348: 'baiyin', 349: 'tianshui', 350: 'wuwei', 351: 'zhangye', 352: 'pingliang', 353: 'jiuquan', 354: 'qingyang', 355: 'dingxi', 356: 'longnan', 357: 'linxia', 358: 'gannan', 
               360: 'xining', 361: 'haidong', 362: 'haibei', 363: 'huangnan', 364: 'hainanzangzu', 365: 'guoluo', 366: 'yushu', 367: 'haixi', 369: 'yinchuan', 370: 'shizuishan', 371: 'wuzhong', 372: 'guyuan', 373: 'zhongwei', 375: 'wulumuqi', 376: 'kelamayi', 377: 'tulufan', 378: 'hami', 379: 'changji', 380: 'boertala', 
               381: 'bayinguoleng', 382: 'akesu', 383: 'kezilesukeerkezi', 384: 'kashi', 385: 'hetian', 386: 'yili', 387: 'tacheng', 388: 'aletai', 389: 'shihezi', 390: 'alaer', 391: 'tumushuke', 392: 'wujiaqu'}

user_tags = {10006: 'Long-term interest/news', 10024: 'Long-term interest/education', 10031: 'Long-term interest/automobile', 10048: 'Long-term interest/real estate', 10052: 'Long-term interest/IT', 10057: 'Long-term interest/electronic game', 10059: 'Long-term interest/fashion', 10063: 'Long-term interest/entertainment', 
             10067: 'Long-term interest/luxury', 10074: 'Long-term interest/home and lifestyle', 10075: 'Long-term interest/health', 10076: 'Long-term interest/food', 10077: 'Long-term interest/divine', 10079: 'Long-term interest/motherhood&parenting', 10083: 'Long-term interest/sports', 10093: 'Long-term interest/travel&outdoors', 
             10102: 'Long-term interest/social', 10684: 'In-market/3c product', 11092: 'In-market/appliances', 11278: 'In-market/clothing、shoes&bags', 11379: 'In-market/Beauty& Personal Care', 11423: 'In-market/household&home improvement', 11512: 'In-market/infant&mom products', 11576: 'In-market/sports item', 
             11632: 'In-market/outdoor', 11680: 'In-market/health care products', 11724: 'In-market/luxury', 11944: 'In-market/real estate', 13042: 'In-market/automobile', 13403: 'In-market/finance', 13496: 'In-market/travel', 13678: 'In-market/education', 13776: 'In-market/service', 13800: 'Long-term interest/art&photography&design', 
             13866: 'Long-term interest/online literature', 13874: 'In-market/electronic game', 14273: 'Long-term interest/3c', 16593: 'In-market/book', 16617: 'In-market/medicine', 16661: 'In-market/food&drink', 16706: 'Long-term interest/culture', 16751: 'Long-term interest/sex', 10110: 'Demographic/gender/male', 10111: 'Demographic/gender/famale'}

advertisers = {1458: 'Chinese vertical e-commerce', 3358: 'Software', 3386: 'International e-commerce', 3427: 'Oil', 3476: 'Tire', 2259: 'Milk powder', 2261: 'Telecom', 2821: 'Footwear', 2997: 'Mobile e-commerce app install'}

def get_region(region_id):
    return region_dict[region_id]

def get_city(city_id):
    return cities_dict[city_id]

def get_user_tags(user_tag_ids):
    if user_tag_ids == float('nan'):
        return ''
    tags = []
    try:
        for tag in user_tag_ids.split(','):
            tags.append(user_tags[int(tag)])
    except:
        pass
    return ','.join(tags)

def get_advertiser(advertiser_id):
    return advertisers[advertiser_id]