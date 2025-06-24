from typing import Optional, Tuple

import gradio
import os

from facefusion import state_manager, wording
from facefusion.face_store import clear_reference_faces, clear_static_faces
from facefusion.filesystem import is_image, is_video
from facefusion.uis.core import register_ui_component
from facefusion.uis.types import ComponentOptions, File

TARGET_FILE : Optional[gradio.File] = None
TARGET_PATH_INPUT : Optional[gradio.Textbox] = None
TARGET_MODE : Optional[gradio.Radio] = None
TARGET_IMAGE : Optional[gradio.Image] = None
TARGET_VIDEO : Optional[gradio.Video] = None


def render() -> None:
	global TARGET_FILE
	global TARGET_PATH_INPUT
	global TARGET_MODE
	global TARGET_IMAGE
	global TARGET_VIDEO

	is_target_image = is_image(state_manager.get_item('target_path'))
	is_target_video = is_video(state_manager.get_item('target_path'))
	
	# Add mode selector
	TARGET_MODE = gradio.Radio(
		label="Input Mode",
		choices=["Upload File", "Local Path"],
		value="Upload File"
	)
	
	# File upload component
	TARGET_FILE = gradio.File(
		label = wording.get('uis.target_file'),
		value = state_manager.get_item('target_path') if is_target_image or is_target_video else None,
		visible = True
	)
	
	# Path input component
	TARGET_PATH_INPUT = gradio.Textbox(
		label = "Local File Path (in /tmp)",
		placeholder = "/tmp/your_file.jpg",
		value = state_manager.get_item('target_path') if is_target_image or is_target_video else None,
		visible = False
	)
	
	target_image_options : ComponentOptions =\
	{
		'show_label': False,
		'visible': False
	}
	target_video_options : ComponentOptions =\
	{
		'show_label': False,
		'visible': False
	}
	if is_target_image:
		if state_manager.get_item('target_path'):
			target_image_options['value'] = state_manager.get_item('target_path')
		target_image_options['visible'] = True
	if is_target_video:
		if state_manager.get_item('target_path'):
			target_video_options['value'] = state_manager.get_item('target_path')
		target_video_options['visible'] = True
	TARGET_IMAGE = gradio.Image(**target_image_options)
	TARGET_VIDEO = gradio.Video(**target_video_options)
	register_ui_component('target_image', TARGET_IMAGE)
	register_ui_component('target_video', TARGET_VIDEO)


def listen() -> None:
	TARGET_MODE.change(toggle_input_mode, inputs = TARGET_MODE, outputs = [ TARGET_FILE, TARGET_PATH_INPUT ])
	TARGET_FILE.change(update_from_file, inputs = TARGET_FILE, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])
	TARGET_PATH_INPUT.submit(update_from_path, inputs = TARGET_PATH_INPUT, outputs = [ TARGET_IMAGE, TARGET_VIDEO ])


def toggle_input_mode(mode: str) -> Tuple[gradio.File, gradio.Textbox]:
	if mode == "Upload File":
		return gradio.File(visible=True), gradio.Textbox(visible=False)
	else:
		return gradio.File(visible=False), gradio.Textbox(visible=True)


def validate_path(path: str) -> bool:
	"""Validate that the path is within /tmp and exists"""
	if not path:
		return False
	
	# Resolve the absolute path to prevent directory traversal
	abs_path = os.path.abspath(path)
	
	# Check if path is within /tmp
	if not abs_path.startswith('/tmp/'):
		return False
	
	# Check if file exists
	if not os.path.exists(abs_path):
		return False
	
	return True


def update_from_file(file : File) -> Tuple[gradio.Image, gradio.Video]:
	clear_reference_faces()
	clear_static_faces()

	if file and is_image(file.name):
		state_manager.set_item('target_path', file.name)
		return gradio.Image(value = file.name, visible = True), gradio.Video(value = None, visible = False)

	if file and is_video(file.name):
		state_manager.set_item('target_path', file.name)
		return gradio.Image(value = None, visible = False), gradio.Video(value = file.name, visible = True)

	state_manager.clear_item('target_path')
	return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)


def update_from_path(path : str) -> Tuple[gradio.Image, gradio.Video]:
	clear_reference_faces()
	clear_static_faces()

	if not validate_path(path):
		# Invalid path - clear everything
		state_manager.clear_item('target_path')
		return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)

	if is_image(path):
		state_manager.set_item('target_path', path)
		return gradio.Image(value = path, visible = True), gradio.Video(value = None, visible = False)

	if is_video(path):
		state_manager.set_item('target_path', path)
		return gradio.Image(value = None, visible = False), gradio.Video(value = path, visible = True)

	state_manager.clear_item('target_path')
	return gradio.Image(value = None, visible = False), gradio.Video(value = None, visible = False)
