import { useEffect, useState, useRef } from 'react';
import { Folder, FolderOpen, Trash2, Download } from "lucide-react";
import { useTranslation } from "react-i18next";
import { apiFetch } from '../utils/apiFetch';
import Button from './Button';
import toast from 'react-hot-toast';

const formatSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
};

const getFileIcon = (mimeType) => {
  if (!mimeType) return "📎";
  if (mimeType.startsWith("image/")) return "🖼️";
  if (mimeType === "application/pdf") return "📄";
  if (mimeType.includes("video")) return "🎬";
  if (mimeType.includes("word") || mimeType.includes("document")) return "📝";
  if (mimeType.includes("sheet") || mimeType.includes("excel")) return "📊";
  return "📎";
};

export default function FolderSection({
  clientId,
  folderKey,
  folderLabel,
  isOpen,
  onToggle,
  onDelete
}) {
  const [deleting, setDeleting] = useState(false);
  const [files, setFiles] = useState([]);
  const [loadingFiles, setLoadingFiles] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [filesLoaded, setFilesLoaded] = useState(false);
  const { t } = useTranslation();
  const fileInputRef = useRef(null);

  const handleFileSelected = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const { url, file_path } = await apiFetch(`/storage/upload/${clientId}/${folderKey}`, {
        method: 'POST',
        body: JSON.stringify({
          file_name: file.name,
          mime_type: file.type,
        }),
      });

      const uploadResult = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': file.type },
        body: file,
      });
      
      if (!uploadResult.ok) throw new Error(`Upload to R2 failed: ${uploadResult.status}`);

      await apiFetch(`/storage/save-file`, {
        method: 'POST',
        body: JSON.stringify({
          file_path: file_path,
          file_name: file.name,
          mime_type: file.type,
          file_size: file.size,
          folder: folderKey,
          client_id: clientId,
        }),
      });

      const data = await apiFetch(`/storage/list/${clientId}/${folderKey}`);
      setFiles(data || []);
      setFilesLoaded(true);
      toast.success(t('clientDetail.fileUploaded'));
    } catch (e) {
        toast.error(e.message);
    } finally {
        setUploading(false);
        e.target.value = "";
    }
  };

  const handleDeleteFile = async (file) => {
    if (!window.confirm(t('clientDetail.deleteFileConfirm', { name: file.file_name }))) return;
    try {
      await apiFetch(`/storage/delete/${clientId}/${folderKey}/${file.id}`, {
        method: "DELETE",
      });
      setFiles(prev => prev.filter(f => f.id !== file.id));
      toast.success(t('clientDetail.fileDeleted'));
    } catch (e) {
      toast.error(e.message);
    }
  };

  const handleDownloadFile = async (file) => {
    try {
        const { url } = await apiFetch(`/storage/download/${clientId}/${folderKey}/${file.id}`);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.file_name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    } catch (e) {
        toast.error(e.message);
    }
    };

  useEffect(() => {
    if (!isOpen || filesLoaded) return;
    const loadFiles = async () => {
      setLoadingFiles(true);
      try {
        const data = await apiFetch(`/storage/list/${clientId}/${folderKey}`);
        setFiles(data || []);
        setFilesLoaded(true);
      } catch (e) {
        console.error(t('clientDetail.loadFilesError'), e);
      } finally {
        setLoadingFiles(false);
      }
    };
    loadFiles();
  }, [isOpen, filesLoaded]);

  return (
    <div>
      {/* ── Folder Header ── */}
      <div className="flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-gray-50 transition-colors group">
        <button
          onClick={onToggle}
          className="flex items-center gap-2.5 text-sm text-gray-700 flex-1 text-left"
          aria-expanded={isOpen}
        >
          {isOpen
            ? <FolderOpen className="w-4 h-4 text-primary" />
            : <Folder className="w-4 h-4 text-gray-500" />
          }
          {folderLabel}
        </button>
        <button
          onClick={onDelete}
          disabled={deleting}
          aria-label={t('clientDetail.deleteFolder', { name: folderLabel })}
          className="opacity-0 group-hover:opacity-100 focus:opacity-100 p-1 rounded-lg text-gray-500 hover:text-red-500 hover:bg-red-50 transition disabled:opacity-40"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* ── Folder Content ── */}
      {isOpen && (
        <div className="ml-9 mt-1 mb-2 px-3 py-3 bg-gray-50 rounded-xl flex flex-col gap-2">

          {loadingFiles ? (
            <p className="text-xs text-gray-400">{t('clientDetail.loadingFiles')}</p>
          ) : files.length === 0 ? (
            <p className="text-xs text-gray-400 italic">{t('clientDetail.noFiles')}</p>
          ) : (
            <>
              {/* Column headers */}
              <div className="flex items-center gap-3 px-2 pb-1 border-b border-gray-200 mb-1">
                <span className="text-xs text-gray-400 flex-1">{t('clientDetail.fileName')}</span>
                <span className="text-xs text-gray-400 w-16 text-right">{t('clientDetail.fileSize')}</span>
                <span className="w-6" aria-hidden="true" />
              </div>

              {/* File rows */}
              {files.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center gap-3 px-2 py-1.5 rounded-lg hover:bg-white transition-colors group/file"
                >
                  <span className="text-base flex-shrink-0" aria-hidden="true">
                    {getFileIcon(file.mime_type)}
                  </span>
                  <span className="flex-1 truncate text-xs text-gray-700 font-medium">
                    {file.file_name}
                  </span>
                  <span className="text-xs text-gray-400 w-16 text-right flex-shrink-0">
                    {formatSize(file.file_size)}
                  </span>
                  <button
                    onClick={() => handleDownloadFile(file)}
                    aria-label={t('clientDetail.downloadFile', { name: file.file_name })}
                    className="opacity-40 hover:opacity-100 focus:opacity-100 p-1 rounded-lg text-gray-400 hover:text-primary hover:bg-primary/10 transition flex-shrink-0"
                    >
                    <Download className="w-3.5 h-3.5" />
                    </button>
                  <button
                    onClick={() => handleDeleteFile(file)}
                    aria-label={t('clientDetail.deleteFile', { name: file.file_name })}
                    className="opacity-40 hover:opacity-100 focus:opacity-100 p-1 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 transition flex-shrink-0"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </>
          )}

          {/* Upload */}
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileSelected}
            aria-hidden="true"
          />
          <Button
            variant="secondary"
            size="sm"
            onClick={() => fileInputRef.current.click()}
            loading={uploading}
            className="mt-1 w-full"
          >
            {t('clientDetail.uploadFile')}
          </Button>

        </div>
      )}
    </div>
  );
}