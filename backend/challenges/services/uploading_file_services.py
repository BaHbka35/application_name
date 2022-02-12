class UploadFileService:

    @staticmethod
    def is_video_file_valid(data: dict, field: str) -> bool:
        """Validates video file."""
        if field not in data:
            return False
        if not data[field]:
            return False
        if not data[field].name[-3:] == 'mp4':
            return False
        return True
