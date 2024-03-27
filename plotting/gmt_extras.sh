#!/bin/bash

gmt_extras::set_gmt_defaults () {
  gmt set FONT_ANNOT_PRIMARY 7p
  gmt set FONT_LABEL 7p
  gmt set MAP_ANNOT_OFFSET_PRIMARY 2p
  gmt set MAP_LABEL_OFFSET 6p
  gmt set PS_LINE_JOIN round
  gmt set MAP_FRAME_TYPE plain
  gmt set PS_PAGE_ORIENTATION portrait
  gmt set PS_MEDIA a4
  gmt set GMT_VERBOSE n
  gmt set PS_CHAR_ENCODING Standard+
}