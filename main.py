from time import sleep

with open ('login', 'r') as login:
    k = login.readline().split(':')
    log = k[0]
    passw = k[1]
    
import vk_api
vk_auth = vk_api.VkApi(log, passw)
vk_auth.auth()
vk = vk_auth.get_api()

mid = vk.users.get()
myid = mid[0]['id']



def get_wall():
    all_views = 0
    all_likes = 0
    coeff = 0
    acoeff = 0
    count = vk.wall.get()['count']
    checkdom = vk.messages.getHistory(user_id = myid, count = 1)['items'][0]['body']
    if checkdom.find('wall') != -1:
        dom = checkdom.replace('wall ', '')
    if count < 100: count = 100
    wall = vk.wall.get(domain = dom, count = 100, offset = count-100)
    res = []
    for post in wall['items']:
        try:
            all_views += post['views']['count']
            all_likes += post['likes']['count']
            post_views = post['views']['count']
            post_likes = post['likes']['count']
            coeff = float(post_likes) / float(post_views) * 100
            res.append (str(post_views) + ' views, ' + str(post_likes) + ' likes, ' + 'coeff = ' + str(coeff))
        except KeyError:
            print 'kek'
    acoeff = float(all_likes) / float (all_views) * 100
    res.append ('\n avg coeff = ' + str(acoeff))
    resp = '\n'.join(res)
    vk.messages.send(user_id = myid, message = acoeff)
    
while 1==1:
    checkdom = vk.messages.getHistory(user_id = myid, count = 1)['items'][0]['body']
    if checkdom.find('wall') != -1:
        get_wall()
        sleep (2)