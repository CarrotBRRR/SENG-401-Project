export const DetailField = ({
  title,
  value,
}: {
  title: string;
  value?: string | number | null | undefined;
}) => {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="opacity-50 font-semibold">{title}</h2>
      <p className="text-lg font-medium">{value}</p>
    </div>
  );
};
