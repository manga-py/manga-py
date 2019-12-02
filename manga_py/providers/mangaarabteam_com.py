from ._3asq_org import ThreeAsqOrg


class MangaArabTeamCom(ThreeAsqOrg):

    def get_chapter_index(self) -> str:
        return self.chapter.split('/')[-1]

main = MangaArabTeamCom
