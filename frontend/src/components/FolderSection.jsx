import { useState } from 'react';
import { Folder, FolderOpen, Trash2 } from "lucide-react";
import { useTranslation } from "react-i18next";
import { apiFetch } from '../utils/apiFetch';

export default function FolderSection ({
    client_id,
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
    const { t } = useTranslation();

     return (
        <div>
        {/* Folder Header */}
        <div className="flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-gray-50 transition-colors group">
            <button
            onClick={onToggle}
            className="flex items-center gap-2.5 text-sm text-gray-700 flex-1 text-left"
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
            className="opacity-0 group-hover:opacity-100 p-1 rounded-lg text-gray-500 hover:text-red-500 hover:bg-red-50 transition disabled:opacity-40"
            >
            <Trash2 className="w-3.5 h-3.5" />
            </button>
        </div>

        {/* Folder Content while open */}
        {isOpen && (
            <div className="ml-9 mt-1 mb-2 px-3 py-3 bg-gray-50 rounded-xl">
            {/* Aquí irán los archivos y el botón de subir */}
            <p className="text-xs text-gray-500 italic">{t('clientDetail.fileUploadSoon')}</p>
            </div>
        )}
        </div>
    );
}
  

