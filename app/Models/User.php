<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;

use App\Traits\Searchable as TraitsSearchable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    /** @use HasFactory<\Database\Factories\UserFactory> */
    use HasApiTokens, HasFactory, Notifiable, TraitsSearchable;

    /**
     * The attributes that are mass assignable.
     *
     * @var list<string>
     */
    protected $primaryKey = 'id';

    protected $fillable = [
        'name',
        'email',
        'image',
        'password',
        'status',
        'role_id'
    ];

    protected $searchable = ['name'];


    /**
     * The attributes that should be hidden for serialization.
     *
     * @var list<string>
     */
    protected $hidden = [
        'password',
        'remember_token',
    ];

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
            'status' => 'integer',
            'role_id' => 'integer'
        ];
    }


    public function role()
    {
        return $this->belongsTo(Role::class);
    }

    public function isAdmin()
    {
        return $this->role->slug === 'admin';
    }
    public function isInternal()
    {
        return $this->role->slug === 'internal';
    }
    public function isExternal()
    {
        return $this->role->slug === 'external';
    }

    public function hasPermission($permissionSlug)
    {
        if ($this->role && $this->role->permissions->contains('slug', $permissionSlug)) {
            return true;
        }
        return false;
    }

    public function notifications()
    {
        return $this->hasMany(Notification::class, 'id', 'user_id');
    }
}
