from instabot import Bot
import os
import dotenv
import igraph
from collections import deque


class InstaMutualFriends:
    bot = Bot()
    friends_g = igraph.Graph()

    def __init__(self, user_1, user_2, login, password):
        self.user_1 = user_1
        self.user_2 = user_2
        self.login = login
        self.password = password
        self.deque_id = deque()
        self.parse_friends = []

    def run(self):
        self.bot.login(username=self.login, password=self.password)
        start_id = self.bot.get_user_id_from_username(self.user_1)
        target_id = self.bot.get_user_id_from_username(self.user_2)
        self.friends_g.add_vertex(name=start_id)
        path = self._find_mutual_friends(start_id=start_id, target_id=target_id)
        return print(f"{self.friends_g.vs[path[0]]['name']}")

    def _find_mutual_friends(self, start_id, target_id):
        if start_id not in self.friends_g.vs['name']:  # Проверка есть ли такая вершина в графе, что-бы не плодить повт.
            self.friends_g.add_vertex(name=start_id)
        friends = self._get_reciprocity_friends(start_id)
        for friend in friends:
            if friend not in self.friends_g.vs['name']:
                self.friends_g.add_vertex(name=friend)
            self.friends_g.add_edge(start_id, friend)
            if friend not in self.deque_id and friend not in self.parse_friends:  # отсекаем повторы и пройденные старинцы людей в очереди
                self.deque_id.append(friend)
        if not target_id in self.friends_g.vs['name']:
            self.parse_friends.append(start_id)
            return self._find_mutual_friends(self.deque_id.popleft(), target_id)
        else:
            return self.friends_g.get_shortest_paths(self.bot.get_user_id_from_username(self.user_1), target_id)

    def _get_reciprocity_friends(self, user_id):
        followers = self.bot.get_user_followers(user_id=user_id)
        following = self.bot.get_user_following(user_id=user_id)
        friends = []
        for freind in following:  # цикл обработки взаимных подписок
            if freind in followers:
                friends.append(freind)
        return friends


if __name__ == '__main__':
    dotenv.load_dotenv(".env")
    a = InstaMutualFriends(user_1="elonrmuskk", user_2="alexsmithla518", login=os.getenv("INST_LOGIN"),
                           password=os.getenv("INST_PSWORD"))
    a.run()
