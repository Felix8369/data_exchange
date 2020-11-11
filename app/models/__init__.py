from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(object):
    """ Base Model """

    def res_format(self, *args, **kwargs) -> dict:
        """
        返回字典数据
        :param args:
        :param kwargs:
        :return:
        """

        d = dict(self.__dict__)
        d.pop('_sa_instance_state', None)

        for k in list(d):
            if k in kwargs:
                if type(kwargs[k]) == type(True) and not kwargs[k]:
                    d.pop(k, None)
                else:
                    d[k] = kwargs[k]

        return d

    def res_format_only(self, *args, **kwargs) -> dict:
        """
        返回字典数据
        :param args:
        :param kwargs:
        :return:
        """

        d = dict(self.__dict__)
        d.pop('_sa_instance_state', True)

        new_d = {}
        for k in list(d):
            if k in kwargs:
                if type(kwargs[k]) == type(True) and kwargs[k]:
                    new_d[k] = d[k]
                else:
                    new_d[k] = kwargs[k]

        return new_d

    @classmethod
    def get_model_by_fields(cls, **kwargs):
        """
        根据字段筛选字段
        :param kwargs:
        :return:
        """
        all = kwargs.pop("all") if kwargs.get("all") else False
        filters = []
        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                filters.append(cls.__dict__.get(key).in_(value))
            else:
                filters.append(cls.__dict__.get(key) == value)
        if all:
            return cls.query.filter(*filters).all()
        else:
            return cls.query.filter(*filters).first()