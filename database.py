from sqlalchemy import Column, create_engine, Sequence, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("postgresql://ndmuser:Password1@localhost/stcndm")
Session = sessionmaker(bind=engine)

class GrtsRecordTable(Base):
    __tablename__ = 'grts_record_table'
    grts_id = Column(types.INTEGER, Sequence('grts_rec_id_seq'), primary_key=True)
    grts_uuid = Column(types.Unicode(36))
    grts_title_en = Column(types.UnicodeText)
    grts_title_fr = Column(types.UnicodeText)
    grts_scanned = Column(types.DATETIME)
    grts_record_en = Column(types.UnicodeText)
    grts_record_fr = Column(types.UnicodeText)

    def __repr__(self):
        return "<GrtsRecordTable(id='%d', uuid='%s', title='%s')>" % self.grts_id, self.grts_uuid, self.grts_title_en


class GrtsSettingTable(Base):
    __tablename__ = 'grts_setting'
    grts_id = Column(types.INTEGER, Sequence('grts_set_id_seq'), primary_key=True)
    key = Column(types.Unicode(64))
    setting = Column(types.UnicodeText)

    def __repr__(self):
        return "<GrtsSettingTable(id='%d', key='%s', setting='%s')>" % self.grts_id,  self.key, self.setting


def get_setting(key, session):
    the_setting = session.query(GrtsSettingTable).filter_by(key=key).first()
    if the_setting:
        print the_setting.setting


def save_setting(key, value, session):
    the_setting = session.query(GrtsSettingTable).filter_by(key=key).first()
    if not the_setting:
        the_setting = GrtsSettingTable(key=key, setting=value)
    the_setting.key = key
    the_setting.setting = value
    session.add(the_setting)
    session.commit()


def get_session():
    return Session

Base.metadata.create_all(engine)


#def setup(db_url):
#    _metadata = MetaData(db_url)
#    grts_records_table = \
#        Table('grts_records_table', _metadata,
#              Column('grts_id', types.INTEGER, Sequence('grts_id_seq'), primary_key=True),
#              Column('grts_uuid', types.Unicode(36)),
#              Column('grts_title_en', types.UnicodeText),
#              Column('grts_title_fr', types.UnicodeText),
#              Column('grts_scanned', types.DATETIME, timezone=True),
#              Column('grts_record_en', types.UnicodeText),
#              Column('grts_record_fr', types.UnicodeText))
#
#    grts_settings_table = \
#        Table('grts_settings', _metadata,
#              Column('key', types.Unicode(64)),
#              Column('setting', types.UnicodeText))
#
#    if not grts_records_table.exists():
#        try:
#            grts_records_table.create()
#        except Exception as e:
#            if grts_records_table.exists():
#                grts_records_table.drop()
#            raise e
#
#    if not grts_settings_table.exists():
#        try:
#            grts_settings_table.create()
#        except Exception as e:
#            if grts_settings_table.exists():
#                grts_settings_table.drop()
#            raise e