from sqlalchemy.dialects.mysql import INTEGER
from app.models import db, BaseModel


class UserModel(db.Model, BaseModel):
    """
    用户
    """

    __tablename__ = 'user'
    __table_args__ = {
        'comment': '用户表'
    }

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    username = db.Column(db.String(55), nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    display_name = db.Column(db.String(55), nullable=False, comment='显示名称')
    company = db.Column(db.String(60), default='', nullable=False, comment='公司/组织')
    image = db.Column(db.String(1024), default='', nullable=False, comment='图片说明、头像')
    api_token = db.Column(db.String(32), default='', nullable=False, comment='Api_Token')
    token_expires = db.Column(INTEGER(unsigned=True), default=0, nullable=False, comment='Token过期时间')
    login_ip = db.Column(db.String(255), default='', nullable=False, comment='登录IP')
    login_time = db.Column(INTEGER(unsigned=True), default=0, nullable=False, comment='登录时间')
    created_at = db.Column(INTEGER(unsigned=True), default=0, nullable=False, comment='创建时间')
    updated_at = db.Column(INTEGER(unsigned=True), default=0, nullable=False, comment='更新时间')
    deleted_at = db.Column(INTEGER(unsigned=True), default=0, nullable=False, comment='删除时间')


    def __repr__(self):
        return '<User {}>'.format(self.username)
