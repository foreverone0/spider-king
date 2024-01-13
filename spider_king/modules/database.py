from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class PostEntity(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    # 帖子标题
    title: Mapped[str] = Column(String(255))

    # 帖子所属板块id
    src_fid: Mapped[str] = mapped_column(String())

    # 帖子链接
    src_url: Mapped[str] = mapped_column(String())

    # 需要复制到的板块id
    dst_fid: Mapped[str] = mapped_column(String())

    # 发布链接
    dst_url: Mapped[str] = mapped_column(String())

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

    def exist_post(self, src_id: str):
        """
        判断帖子是否存在

        :param src_id
        :return:
        """
        session = Session(bind=self.engine)
        try:
            return session.query(PostEntity).filter(PostEntity.id == src_id).first() is not None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
