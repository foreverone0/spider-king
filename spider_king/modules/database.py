from datetime import datetime

import pytz
from sqlalchemy import Column, String, create_engine, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


def get_local_time():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).replace(tzinfo=None)


class Base(DeclarativeBase):
    pass


class PostEntity(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = Column(String(255))  # 帖子标题
    src_fid: Mapped[str] = Column(String(20))  # 帖子所属板块id
    src_url: Mapped[str] = Column(String)  # 帖子链接
    src_tid: Mapped[str] = Column(String(20))  # 帖子id
    dst_fid: Mapped[str] = Column(String(20))  # 发布板块id
    dst_url: Mapped[str] = Column(String)  # 发布链接
    created_at: Mapped[datetime] = Column(DateTime, default=get_local_time)  # 创建时间

    def __repr__(self):
        return f'<PostEntity(id={self.id}, title={self.title}, src_fid:{self.src_fid}, dst_fid:{self.dst_fid})>'


class SpiderDatabase:
    def __init__(self, connect, echo=False):
        self.engine = create_engine(connect, echo=echo)
        Base.metadata.create_all(self.engine)

    def close(self):
        self.engine.dispose()

    def insert_post(self, post: PostEntity):
        """
        插入一条数据

        :param post
        :return:
        """
        session = Session(bind=self.engine)
        try:
            session.add(post)
            session.commit()
            return post.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def exist_post(self, src_tid: str):
        """
        判断帖子是否存在

        :param src_tid
        :return:
        """
        session = Session(bind=self.engine)
        try:
            return session.query(PostEntity).filter(PostEntity.src_tid == str(src_tid).strip()).first() is not None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
