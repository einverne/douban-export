#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import os
from configparser import ConfigParser

import click

from exporter.book import BookExport
from exporter.movie import MovieExport
from exporter.music import MusicExport
from exporter.notes import NoteExport

CONFIG_PATH = os.path.join(os.environ.get('HOME'), '.douban-export')


def read_config():
    config = ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    return config


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    pass


def save_movie(l, writer):
    for m in l:
        click.echo(m.title)
        writer.writerow([
            m.title,
            m.url,
            m.intro,
            m.tags,
            m.comment,
            m.rating_date,
            m.rating
        ])


def save_book(l, writer):
    for b in l:
        click.echo(b.title)
        writer.writerow([
            b.title,
            b.url,
            b.intro,
            b.tags,
            b.comment,
            b.rating_date,
            b.rating
        ])


def save_music(l, writer):
    for music in l:
        click.echo(music.title)
        writer.writerow([
            music.title,
            music.url,
            music.intro,
            music.tags,
            music.comment,
            music.rating_date,
            music.rating
        ])


@cli.command()
@click.option('-u', '--userid', required=False, help='user id')
@click.option('-t', '--type', required=False,
              type=click.Choice(['collect', 'wish', 'doing']),
              default='collect',
              help='type of list, collect, wish, doing')
@click.option('-o', '--outfile', help='output filename')
def movie(userid, type, outfile):
    if not userid:
        config = read_config()
        if 'auth' in config and 'username' in config['auth']:
            userid = config['auth']['username']
        else:
            click.echo("run setup first or pass -u parameter")
            return
    movie_exporter = MovieExport(userid)
    fout = codecs.open(outfile, mode='w', encoding='utf-8')
    writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    if type == 'collect':
        save_movie(movie_exporter.get_watched(), writer)
    elif type == 'wish':
        save_movie(movie_exporter.get_wish(), writer)
    elif type == 'doing':
        save_movie(movie_exporter.get_doing(), writer)
    fout.close()


@cli.command()
@click.option('-u', '--userid', required=False, help='user id')
@click.option('-t', '--type', required=False,
              type=click.Choice(['collect', 'wish', 'doing']),
              default='collect',
              help='type of list, collect, wish, doing')
@click.option('-o', '--outfile', help='output filename')
def book(userid, type, outfile):
    if not userid:
        config = read_config()
        if 'auth' in config and 'username' in config['auth']:
            userid = config['auth']['username']
        else:
            click.echo('run setup first or pass -u parameter')
            return
    exporter = BookExport(userid)
    fout = codecs.open(outfile, mode='w', encoding='utf-8')
    writer = csv.writer(fout, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    if type == 'collect':
        save_book(exporter.get_read(), writer)
    elif type == 'wish':
        save_book(exporter.get_wish(), writer)
    elif type == 'doing':
        save_book(exporter.get_reading(), writer)
    fout.close()


@cli.command()
@click.option('-u', '--userid', required=False, help='user id')
@click.option('-t', '--type', required=False,
              type=click.Choice(['collect', 'wish', 'doing']),
              default='collect',
              help='type of list, collect, wish, doing')
@click.option('-o', '--outfile', help='output filename')
def music(userid, type, outfile):
    if not userid:
        config = read_config()
        if 'auth' in config and 'username' in config['auth']:
            userid = config['auth']['username']
        else:
            click.echo('run setup first or pass -u parameter')
            return
    exporter = MusicExport(userid)
    fout = codecs.open(outfile, mode='w', encoding='utf-8')
    writer = csv.writer(fout, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    if type == 'collect':
        save_music(exporter.get_listened(), writer)
    elif type == 'wish':
        save_music(exporter.get_wish(), writer)
    elif type == 'doing':
        save_music(exporter.get_doing(), writer)
    fout.close()


def save_note(notes, writer):
    for note in notes:
        writer.writerow([
            note.title,
            note.url,
            note.id,
            note.content,
            note.publish_time
        ])


@cli.command()
@click.option('-u', '--userid', required=False, help='user id')
@click.option('-o', '--outfile', help='output filename')
def note(userid, outfile):
    if not userid:
        config = read_config()
        if 'auth' in config and 'username' in config['auth']:
            userid = config['auth']['username']
        else:
            click.echo('run setup first or pass -u parameter')
            return
    exporter = NoteExport(userid)
    fout = codecs.open(outfile, mode='w', encoding='utf-8')
    writer = csv.writer(fout, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    save_note(exporter.get_notes(), writer)
    fout.close()


@cli.command()
def setup():
    """set up username"""
    config = read_config()
    if 'auth' in config and 'username' in config['auth']:
        click.echo("username already setup: " + config['auth']['username'])
        return
    username = input("UserId: ").strip()
    config['auth'] = {'username': username}
    with codecs.open(CONFIG_PATH, mode='w', encoding='utf-8') as fconfig:
        config.write(fconfig)


if __name__ == '__main__':
    cli()
