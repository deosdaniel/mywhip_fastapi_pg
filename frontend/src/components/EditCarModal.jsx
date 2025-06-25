import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from "@/components/ui/dialog";
import CarEditForm from "./CarEditForm";

export default function EditCarModal({formData, setFormData, onSave, onClose, statuses}) {
    return (
        <Dialog open={true} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-2xl w-full max-h-[70vh] overflow-y-auto p-6">
                <DialogHeader>
                    <DialogTitle>Редактировать автомобиль</DialogTitle>
                </DialogHeader>

                <CarEditForm
                    formData={formData}
                    setFormData={setFormData}
                    onSave={onSave}
                    onCancel={onClose}
                    statuses={statuses}
                />
            </DialogContent>
        </Dialog>
    );
}